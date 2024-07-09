import requests
import json
import aiohttp
import asyncio
from urllib.parse import quote

#调用文字识别api retrun response_dict = json.loads(response.text)
# def get_sensitive_words(url, text):
#     body = {
#         'text': text
#     }
#     response = requests.get(url, params=body)
#     response_dict = json.loads(response.text)
#     return response_dict
async def get_sensitive_words_async( text):
    url = 'https://api.pearktrue.cn/api/sensitivewords/'
    params = {
        'text': text
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            response_text = await response.text()
            print(response_text)
            response_dict = json.loads(response_text)
            return response_dict
# 百度敏感词url
async def get_baidu_sensitive_words_async( text):
    url = "https://aip.baidubce.com/rest/2.0/solution/v1/text_censor/v2/user_defined?access_token=24.ce06ae622a94d5a389b2c4cacbd18d57.2592000.1723081565.282335-92517041"
    encoded_text = quote(text)
    payload = 'text=' + encoded_text
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload, headers=headers) as response:
            response_text = await response.text()
            response_dict = json.loads(response_text)
            return response_dict
#用百度url的主函数
async def sensitive_ai_baidu_async(text):
    response_dict = await get_baidu_sensitive_words_async( text)
    print(response_dict)
    if response_dict['conclusion'] == "合规":
        result_dict = dict(response_dict=response_dict, positions="no", positions_dict="no")
        return result_dict
    data = response_dict['data']
    inputtext = text
    all_positions=[]
    all_sensitive_word_dict={}
    for item in data:
        for iitem in item['hits']:
            for iiitem in iitem['wordHitPositions']:
                word_position=[]
                for iiiitem in iiitem['positions']:
                    begin_num=iiiitem[0]
                    end_num=iiiitem[1]
                    result_list = list(range(begin_num, end_num + 1))
                    all_positions.extend(result_list)
                    word_position.extend(result_list)
                word_position = list(set(word_position))  # 去除重复项
                all_sensitive_word_dict[iiitem['keyword']]=word_position
    all_positions = list(set(all_positions))
    # positions =  find_character_positions(result_text, '*')
    # positions_dict =  get_character_positions(inputtext, result_detected_words)
    result_dict = dict(response_dict=response_dict, positions=all_positions, positions_dict=all_sensitive_word_dict)
    return result_dict

# 查找字符比如：*在句子中的位置
def find_character_positions(text, character):
    positions = []
    index = -1
    while True:
        index = text.find(character, index + 1)
        if index == -1:
            break
        positions.append(index)
    return positions
# 每个敏感词出现的位置，可以有多个 ###return positions_dict = {}
def get_character_positions(result_inputtext, result_detected_words):
    ### 每个敏感词出现的位次 ###
    positions_dict = {}  # 用来存储每个词组对应的位置
    for characters in result_detected_words:
        positions = []  # 存储当前词组的所有位置
        start_index = -1
        while True:
            start_index = result_inputtext.find(characters, start_index + 1)
            if start_index == -1:
                break
            else:
                #positions.append(start_index)
                for i in range(len(characters)):
                    positions.append(start_index+i)
        positions_dict[characters] = positions
    return positions_dict
# print信息
def print_information(response_dict,StatusCode,datatext,positions,positions_dict):
    print(response_dict)
    print('Status Code:', StatusCode)#response_dict['code']
    print(datatext)#data['text']
    print("所有'*'的位置：", positions)
    print("每个词组对应的位置如下：")
    for characters, positions in positions_dict.items():
        print("词组“{}”的位置：{}".format(characters, positions))
# 主函数
# def sensitive_ai(text):
#     url = 'https://api.pearktrue.cn/api/sensitivewords/'
#     response_dict = get_sensitive_words(url, text) # 不同url的接口此调用函数不通用。
#     #print(response_dict)
#     #'msg': '文本内没有敏感词'
#     if response_dict['msg']=='文本内没有敏感词':
#         result_dict = dict(response_dict=response_dict, positions="no", positions_dict="no")
#         return result_dict
#     data = response_dict['data']  # 取出data的值
#     inputtext = response_dict['inputtext']
#     result_text = data['text']
#     result_detected_words = data['detected_words']
#
#     positions = find_character_positions(result_text, '*')
#     positions_dict = get_character_positions(inputtext, result_detected_words)
#     #输出
#     #print_information(response_dict, response_dict['code'], data['text'], positions, positions_dict)
#     result_dict = dict(response_dict=response_dict, positions=positions, positions_dict=positions_dict)
#     return result_dict
# 不用百度url的主函数
async def sensitive_ai_async(text):
    response_dict = await get_sensitive_words_async( text)
    if response_dict['msg'] == '文本内没有敏感词':
        result_dict = dict(response_dict=response_dict, positions="no", positions_dict="no")
        return result_dict
    data = response_dict['data']
    inputtext = response_dict['inputtext']
    result_text = data['text']
    result_detected_words = data['detected_words']
    positions =  find_character_positions(result_text, '*')
    positions_dict =  get_character_positions(inputtext, result_detected_words)
    result_dict = dict(response_dict=response_dict, positions=positions, positions_dict=positions_dict)
    return result_dict

if __name__ == '__main__':
    #str='直方图均衡化后面潜在的数学原理是一个分布（输人的亮度直方图）被映射到另一个分布（一个更宽，理想统一的亮度值分布）。也就是说，我们希望把原始分布中轴的值在新分布中尽可能展开。这说明对拉伸数值分布的问题我们有一个比较好的答案：映射函数应该是一个累积分布函数。图6．23是一个累积密度丞数的例子，这'
    # str='我要杀掉所有人,常念法轮大法好，杀杀杀'
    str='敏感词检测pdf，武力统一台湾，常念法轮大法好，我的银行卡号是1342213，我的身份证号是52314123'
    loop = asyncio.get_event_loop()
    result_dict=loop.run_until_complete(sensitive_ai_async(str))
    print(result_dict)
