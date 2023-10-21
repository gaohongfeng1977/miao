import zhipuai

# your api key
zhipuai.api_key = "df07a1933b31afb1f51721471cdb5621.S80rPNUyz0R9q1Gu"

def invoke_example():
    response = zhipuai.model_api.invoke(
        model="chatglm_pro",
           prompt=[
                    {"role": "user", "content": "你好"},
                    {"role": "assistant", "content": "我是宠物医生，擅长对犬类和猫类病症的诊断。"},                    
                    {"role":"user", "content": "请问我的宠物狗骨折了，怎么治疗？"},
                ],
        top_p=0.7,
        temperature=0.9,
    )
    print(response)

def async_invoke_example():
    response = zhipuai.model_api.async_invoke(
        model="chatglm_pro",
        prompt=[{"role": "user", "content": "人工智能"}],
        top_p=0.7,
        temperature=0.9,
    )
    print(response)


invoke_example()