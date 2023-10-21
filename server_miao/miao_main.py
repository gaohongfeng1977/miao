import mimetypes
import os
from typing import Union
import cv2
import requests
import torch
import transformers
from PIL import Image
import sys
import time
import shutil
import zhipuai


sys.path.append("../../src")
# make sure you can properly access the otter folder
from otter_ai import OtterForConditionalGeneration

# Disable warnings
requests.packages.urllib3.disable_warnings()

# ------------------- Utility Functions -------------------


def get_content_type(file_path):
    content_type, _ = mimetypes.guess_type(file_path)
    return content_type


# ------------------- Image and Video Handling Functions -------------------


def extract_frames(video_path, num_frames=16):
    video = cv2.VideoCapture(video_path)
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_step = total_frames // num_frames
    frames = []

    for i in range(num_frames):
        video.set(cv2.CAP_PROP_POS_FRAMES, i * frame_step)
        ret, frame = video.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = Image.fromarray(frame).convert("RGB")
            frames.append(frame)

    video.release()
    return frames


def get_image(url: str) -> Union[Image.Image, list]:
    if "://" not in url:  # Local file
        content_type = get_content_type(url)
    else:  # Remote URL
        content_type = requests.head(url, stream=True, verify=False).headers.get("Content-Type")

    if "image" in content_type:
        if "://" not in url:  # Local file
            return Image.open(url)
        else:  # Remote URL
            return Image.open(requests.get(url, stream=True, verify=False).raw)
    elif "video" in content_type:
        video_path = "temp_video.mp4"
        if "://" not in url:  # Local file
            video_path = url
        else:  # Remote URL
            with open(video_path, "wb") as f:
                f.write(requests.get(url, stream=True, verify=False).content)
        frames = extract_frames(video_path)
        if "://" in url:  # Only remove the temporary video file if it was downloaded
            os.remove(video_path)
        return frames
    else:
        raise ValueError("Invalid content type. Expected image or video.")


# ------------------- OTTER Prompt and Response Functions -------------------


def get_formatted_prompt(prompt: str) -> str:
    return f"<image>User: {prompt} GPT:<answer>"


def get_response(input_data, prompt: str, model=None, image_processor=None, tensor_dtype=None) -> str:
    if isinstance(input_data, Image.Image):
        vision_x = image_processor.preprocess([input_data], return_tensors="pt")["pixel_values"].unsqueeze(1).unsqueeze(0)
    elif isinstance(input_data, list):  # list of video frames
        vision_x = image_processor.preprocess(input_data, return_tensors="pt")["pixel_values"].unsqueeze(0).unsqueeze(0)
    else:
        raise ValueError("Invalid input data. Expected PIL Image or list of video frames.")

    lang_x = model.text_tokenizer(
        [
            get_formatted_prompt(prompt),
        ],
        return_tensors="pt",
    )

    # Get the data type from model's parameters
    model_dtype = next(model.parameters()).dtype

    # Convert tensors to the model's data type
    vision_x = vision_x.to(dtype=model_dtype)
    lang_x_input_ids = lang_x["input_ids"]
    lang_x_attention_mask = lang_x["attention_mask"]

    bad_words_id = model.text_tokenizer(["User:", "GPT1:", "GFT:", "GPT:"], add_special_tokens=False).input_ids
    generated_text = model.generate(
        vision_x=vision_x.to(model.device),
        lang_x=lang_x_input_ids.to(model.device),
        attention_mask=lang_x_attention_mask.to(model.device),
        max_new_tokens=512,
        num_beams=3,
        no_repeat_ngram_size=3,
        bad_words_ids=bad_words_id,
    )
    parsed_output = (
        model.text_tokenizer.decode(generated_text[0])
        .split("<answer>")[-1]
        .lstrip()
        .rstrip()
        .split("<|endofchunk|>")[0]
        .lstrip()
        .rstrip()
        .lstrip('"')
        .rstrip('"')
    )
    return parsed_output




def api_zhipu(prompt: str) -> str:
    response = zhipuai.model_api.invoke(
        model="chatglm_pro",
           prompt=[
                    {"role": "user", "content": "你好"},
                    {"role": "assistant", "content": "我是宠物医生，擅长对犬类和猫类病症的诊断。"},                    
                    {"role":"user", "content": f"1.将中括号内容反映称中文内容；2.将中文内容进行风格化；中括号为内容如下[{prompt}]"},
                ],
        top_p=0.7,
        temperature=0.8,
    )
    return f"response: {response}"


#======================================================
# ------------------- Main Function -------------------
#======================================================

#1.model init

load_bit = "fp16"
if load_bit == "fp16":
    precision = {"torch_dtype": torch.float16}
elif load_bit == "bf16":
    precision = {"torch_dtype": torch.bfloat16}
elif load_bit == "fp32":
    precision = {"torch_dtype": torch.float32}

# This model version is trained on MIMIC-IT DC dataset.
model = OtterForConditionalGeneration.from_pretrained("/data/opexlab", device_map="auto", **precision)
tensor_dtype = {"fp16": torch.float16, "bf16": torch.bfloat16, "fp32": torch.float32}[load_bit]

model.text_tokenizer.padding_side = "left"
tokenizer = model.text_tokenizer
image_processor = transformers.CLIPImageProcessor()
model.eval()

# zhipu app key
zhipuai.api_key = "df07a1933b31afb1f51721471cdb5621.S80rPNUyz0R9q1Gu"

#2.start inference epoch

mediatype = "video"
mainpath = "/home/ec2-user/"

media_dir = os.path.join(mainpath , "datasource/" , mediatype )  # video path/.
backup_media_dir = os.path.join(mainpath , "processedsource/" , mediatype )

#----------debug segments start-------------
#datasource initial
for dirpath, dirnames, filenames in os.walk(backup_media_dir):
            for filename in filenames:
                file_url = os.path.join(dirpath,filename)
                shutil.move(file_url, media_dir)

#----------debug segments end ---------------

while True:

    media_dir = os.path.join(mainpath , "datasource/" , mediatype )  # video path/.
    #循环目录每个文件，进行预测
    for dirpath, dirnames, filenames in os.walk(media_dir):
            for filename in filenames:
                file_url = os.path.join(dirpath,filename)

                #TODO: check if file is writted or uploaded


                frames_list = get_image(file_url)
                prompts_input = "what is the picture tell us ?"
                response = get_response(frames_list, prompts_input, model, image_processor, tensor_dtype)
                print(f"Response: {response}")

                #send info to zhipu api
                response = api_zhipu(response)
                print(f"Response: {response}")

                #backup media current file
                shutil.move(file_url, backup_media_dir)


                time.sleep(1) #for debug 