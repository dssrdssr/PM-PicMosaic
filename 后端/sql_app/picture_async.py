import json
from urllib.parse import quote
import aiohttp
import asyncio


#https://api.pearktrue.cn/info?id=206
# 识别图中文字的url
# def get_picture_words(url, image_url):
#     data = {"file": image_url}
#     response = requests.post(url, headers={"Content-Type": "application/json"}, data=json.dumps(data))
#     response_dict = response.json()
#     return response_dict
async def get_picture_words_async(url, image_url):
    data = {"file": image_url}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers={"Content-Type": "application/json"}, data=json.dumps(data)) as response:
            response_dict = await response.json()
            return response_dict

# def url_baidu(image_url):
#     url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general?access_token=24.1de6e7d9a2dfe2e6325ac2ecec1c79e1.2592000.1722876645.282335-91530730"
#     encoded_image_url = quote(image_url)
#     payload = 'url='+encoded_image_url+'&recognize_granularity=small&detect_direction=false&detect_language=false&vertexes_location=true&paragraph=false&probability=true'
#     headers = {
#         'Content-Type': 'application/x-www-form-urlencoded',
#         'Accept': 'application/json'
#     }
#     response = requests.request("POST", url, headers=headers, data=payload)
#     response_dict = response.json()
#     return response_dict
async def url_baidu_async(image_url):
    url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general?access_token=24.1de6e7d9a2dfe2e6325ac2ecec1c79e1.2592000.1722876645.282335-91530730"
    encoded_image_url = quote(image_url)
    payload = 'url='+encoded_image_url+'&recognize_granularity=small&detect_direction=false&detect_language=false&vertexes_location=true&paragraph=false&probability=true'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload, headers=headers) as response:
            response_dict = await response.json()
            return response_dict

# def base64_baidu(image_base64):
#     url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general?access_token=24.1de6e7d9a2dfe2e6325ac2ecec1c79e1.2592000.1722876645.282335-91530730"
#     encoded_image_base64 = quote(image_base64)
#     payload = 'image='+encoded_image_base64+'&recognize_granularity=small&detect_direction=false&detect_language=false&vertexes_location=true&paragraph=false&probability=true'
#     headers = {
#         'Content-Type': 'application/x-www-form-urlencoded',
#         'Accept': 'application/json'
#     }
#     response = requests.request("POST", url, headers=headers, data=payload)
#     response_dict = response.json()
#     return response_dict
async def base64_baidu_async(image_base64):
    url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general?access_token=24.1de6e7d9a2dfe2e6325ac2ecec1c79e1.2592000.1722876645.282335-91530730"
    encoded_image_base64 = quote(image_base64)
    payload = 'image='+encoded_image_base64+'&recognize_granularity=small&detect_direction=false&detect_language=false&vertexes_location=true&paragraph=false&probability=true'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload, headers=headers) as response:
            response_dict = await response.json()
            return response_dict
# print信息
def print_information(code,one_line_text,many_line_text,single_text):
    print("code: ",code)
    print("many_line_text: ", many_line_text)
    print("one_line_text: ", one_line_text)
    print("single_text: ", single_text)
    print("\n\n\n")

# 主函数
async def picture_ocr_async(image_url):
    url = "https://api.pearktrue.cn/api/ocr/"
    #response_dict = await get_picture_words_async(url, image_url) # 不同url的接口此调用函数不通用。
    response_dict  = await get_picture_words_async(url, image_url)
    code = response_dict['code']  # 取出data的值
    data = response_dict['data']  # 取出data的值
    many_line_text = data['TextLine']
    one_line_text=data['ParsedText']# 用\r\n表示换行
    result_text = "".join(many_line_text)
    #print_information(code, one_line_text, many_line_text,result_text)
    result_dict = dict(result_text=result_text, response_dict=response_dict)
    return result_dict

if __name__ == '__main__':
    image_url = "http://dl2.iteye.com/upload/attachment/0129/4482/19f369de-84a5-3813-b220-86a27b950837.png"
    loop = asyncio.get_event_loop()
    result_dict=loop.run_until_complete(picture_ocr_async(image_url))
