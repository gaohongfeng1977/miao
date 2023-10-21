#!/user/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# @File : te_006.py
# @Time : 2022-08-11 16:45
# @Author : mojin
# @Email : 397135766@qq.com
# @Software : PyCharm
#-------------------------------------------------------------------------------

import flask, json
from flask import request
from flask_cors import CORS
import zhipuai
'''
flask： web框架，通过flask提供的装饰器@server.route()将普通函数转换为服务
pip3 install flask -i https://pypi.doubanio.com/simple

'''
# 创建一个服务，把当前这个python文件当做一个服务
server = flask.Flask(__name__)

# r'/*' 是通配符，让本服务器所有的 URL 都允许跨域请求
CORS(server, resources=r'/*')
zhipuai.api_key = "df07a1933b31afb1f51721471cdb5621.S80rPNUyz0R9q1Gu"
# server.config['JSON_AS_ASCII'] = False
# @server.route()可以将普通函数转变为服务 的路径、请求方式
@server.route('/getquest', methods=['get'])#'get',
def getquest():
    '''
    http://127.0.0.1:5000/list/project?project=324324&name=234
    :return:
    '''
    prompt= request.values.get('quest')
     
    response = zhipuai.model_api.invoke(
    model="chatglm_pro",
       prompt=[
                {"role": "user", "content": "你好"},
                {"role": "assistant", "content": "你是宠物医生，擅长对犬类和猫类病症的诊断。"},                    
                {"role":"user", "content": f"{prompt}"},
            ],
    top_p=0.7,
    temperature=0.8,
    )

    return response



# server.config['JSON_AS_ASCII'] = False
# @server.route()可以将普通函数转变为服务 的路径、请求方式


@server.route('/postquest',methods=['post']) #入参为json
def postquest():
    '''
    http://127.0.0.1:5000/login
    {
    "user_name":"mojin",
    "pwd":"123456"
    }
    :return:
    '''
    params = flask.request.json#当客户端没有传json类型或者没传时候，直接get就会报错。
    # params = flask.request.json #入参是字典时候用这个。
    if params:
        promt = params.get('quest')
        # login_info={
        #     "data": {
        #         "id": 500,
        #         "rid": 0,
        #         "username": dic['user_name'],
        #         "pwd": '*********',
        #         "mobile": "12345678",
        #         "email": "adsfad@qq.com",
        #         "token": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOjUwMCwicmlkIjowLCJpYXQiOjE2NjAyMDcwNTksImV4cCI6MTY2MDI5MzQ1OX0.tt0dOAFrlwckl3yvz1n9r_GLSyaev4kkxzL3jJACYuM"
        #     },
        #     "meta": {
        #         "msg": "登录成功",
        #         "status": 200
        #     }
        # }

        
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
    
        return response


    else:
        #data = json.dumps({"result_code": 3002, "msg": "入参必须为json类型。"})
        data = ({"result_code": 3002, "msg": "入参必须为json类型。"})
        # print("'/getquest',methods=['post']："+str(data))
        return data

if __name__ == '__main__':

    server.run(host='0.0.0.0', port=8089, debug=True)

