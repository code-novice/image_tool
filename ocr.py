# encoding:utf-8
import requests
import base64
from fanyi import *

def ocr():
    # client_id 为官网获取的AK， client_secret 为官网获取的SK
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=&client_secret='
    response = requests.get(host)
    token = response.json()['access_token']


    '''
    通用文字识别（高精度版）
    '''
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"
    # 二进制方式打开图片文件
    f = open('1.png', 'rb')
    img = base64.b64encode(f.read())

    params = {"image":img, "language_type" : 'CHN_ENG'}
    access_token = token
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        query = ''
        for words in response.json()['words_result']:
            query = query + '\n' + words['words']

    fanyi(query)

if __name__ == '__main__':
    ocr()