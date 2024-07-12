from . import sensitive_async,picture_async,user_word
# import sensitive_async,picture_async,user_word
import asyncio
from collections import defaultdict
import time
# url 不用百度的敏感词
async def use_image_url_async(image_url):
    text_dict = await picture_async.url_baidu_async(image_url)
    words_result = text_dict['words_result']  # words_result
    words_result_num = text_dict['words_result_num']  # words_result_num
    log_id = text_dict['log_id']  # log_id
    all_line_position = []
    len_words_result = 0
    all_char_location = []
    for i in range(len(words_result)):
        len_words_result = len_words_result + 1
        text = words_result[i]['words']  # 对每个成员进行操作
        chars = words_result[i]['chars']
        print("待检测语句", text)
        sensitive_dict = await sensitive_async.sensitive_ai_async(text)
        positions = sensitive_dict['positions']
        positions_dict = sensitive_dict['positions_dict']
        print("所有敏感词位置", positions)
        one_line_all_char_position = []
        if positions != 'no':
            for i in positions:
                all_char_location.append(chars[int(i)])
            for characters, positions_characters in positions_dict.items():
                if positions_characters:
                    result_location = [chars[i] for i in positions_characters]
                    # print(positions)
                    print("词组“{}”对应的元素：{}".format(characters, result_location))
                else:
                    characters = []
                    result_location = []
                    print("词组“{}”对应的元素：空列表".format(characters))
                characters_result_location = dict(characters=characters, result_location=result_location)
                one_line_all_char_position.append(characters_result_location)
        one_line_position = dict(text=text, positions=positions, one_line_all_char_position=one_line_all_char_position)
        all_line_position.append(one_line_position)
    #print(all_char_location)
    result_dict = dict(len_words_result=len_words_result, all_line_position=all_line_position,
                       all_char_location=all_char_location)
    print(result_dict)
    return result_dict
# url 不用百度的敏感词 有自选词  *************
async def use_image_url_word_async(image_url,word_list):
    text_dict = await picture_async.url_baidu_async(image_url)
    print(text_dict)
    words_result = text_dict['words_result']  # words_result
    words_result_num = text_dict['words_result_num']  # words_result_num
    log_id = text_dict['log_id']  # log_id
    all_line_position = []
    len_words_result = 0
    all_char_location = []
    for i in range(len(words_result)):
        len_words_result = len_words_result + 1
        text = words_result[i]['words']  # 对每个成员进行操作
        chars = words_result[i]['chars']
        print("待检测语句", text)
        sensitive_dict = await sensitive_async.sensitive_ai_baidu_async(text)
        positions = sensitive_dict['positions']  # 从此开始改变，直到合并字典
        positions_dict_sensitive = sensitive_dict['positions_dict']
        word_dict = user_word.find_word_position_regex(text, word_list)  # 用户自定义词组
        word_positions = word_dict['positions']
        word_positions_dict = word_dict['positions_dict']
        if positions != 'no':
            positions = positions + word_positions
            positions = list(set(positions))  # 去除重复项
        elif word_positions:
            positions = word_positions
        print("所有敏感词位置", positions)
        one_line_all_char_position = []
        if positions != 'no':
            positions_dict = defaultdict(list)
            for d in (positions_dict_sensitive, word_positions_dict):
                for key, value in d.items():
                    positions_dict[key].append(value)
            positions_dict = dict(positions_dict)  # 合并字典
            positions_dict = {key: value[0] for key, value in positions_dict.items()}
        # print("所有敏感词位置", positions)
        # one_line_all_char_position = []
        # if positions != 'no':
            for i in positions:
                all_char_location.append(chars[int(i)])
            for characters, positions_characters in positions_dict.items():
                if positions_characters:
                    result_location = [chars[i] for i in positions_characters]
                    # print(positions)
                    print("词组“{}”对应的元素：{}".format(characters, result_location))
                else:
                    characters = []
                    result_location = []
                    print("词组“{}”对应的元素：空列表".format(characters))
                characters_result_location = dict(characters=characters, result_location=result_location)
                one_line_all_char_position.append(characters_result_location)
        one_line_position = dict(text=text, positions=positions, one_line_all_char_position=one_line_all_char_position)
        all_line_position.append(one_line_position)
    #print(all_char_location)
    result_dict = dict(len_words_result=len_words_result, all_line_position=all_line_position,
                       all_char_location=all_char_location)
    print(result_dict)
    return result_dict
# base64 不用百度的敏感词
async def use_image_base64_async(image_base64):
    text_dict=await  picture_async.base64_baidu_async(image_base64)
    words_result = text_dict['words_result']  # words_result
    words_result_num = text_dict['words_result_num']  # words_result_num
    log_id = text_dict['log_id']  # log_id
    all_line_position=[]
    len_words_result=0
    all_char_location=[]
    for i in range(len(words_result)):
        len_words_result=len_words_result+1
        text=words_result[i]['words']  # 对每个成员进行操作
        chars=words_result[i]['chars']
        print("待检测语句",text)
        sensitive_dict = await sensitive_async.sensitive_ai_async(text)
        positions=sensitive_dict['positions']
        positions_dict=sensitive_dict['positions_dict']
        print("所有敏感词位置",positions)
        one_line_all_char_position=[]
        if positions!='no':
            for i in positions:
                all_char_location.append(chars[int(i)])
            for characters, positions_characters in positions_dict.items():
                if positions_characters:
                    result_location = [chars[i] for i in positions_characters]
                    #print(positions)
                    print("词组“{}”对应的元素：{}".format(characters, result_location))
                else:
                    characters=[]
                    result_location=[]
                    print("词组“{}”对应的元素：空列表".format(characters))
                characters_result_location = dict(characters=characters,result_location=result_location)
                one_line_all_char_position.append(characters_result_location)
        one_line_position = dict(text=text, positions=positions,one_line_all_char_position=one_line_all_char_position)
        all_line_position.append(one_line_position)
    #print(all_char_location)
    result_dict = dict(len_words_result=len_words_result, all_line_position=all_line_position,all_char_location=all_char_location)
    print(result_dict)
    return result_dict
# base64 不用百度的敏感词 有自选词  *************
async def use_image_base64_word_async(image_base64,word_list):
    text_dict=await  picture_async.base64_baidu_async(image_base64)
    print(text_dict)
    if text_dict['words_result'] == []:
        result_dict = dict(len_words_result=-1, all_line_position=-1, all_char_location=-1)
        print(result_dict)
        return result_dict
    words_result = text_dict['words_result']  # words_result
    words_result_num = text_dict['words_result_num']  # words_result_num
    log_id = text_dict['log_id']  # log_id
    all_line_position=[]
    len_words_result=0
    all_char_location=[]
    for i in range(len(words_result)):
        len_words_result=len_words_result+1
        text=words_result[i]['words']  # 对每个成员进行操作
        chars=words_result[i]['chars']
        print("待检测语句",text)
        sensitive_dict = await sensitive_async.sensitive_ai_async(text)
        positions_all_line_re, positions_dict_sensitive_all_line_re = user_word.find_re([], [], text)
        print(sensitive_dict)
        if sensitive_dict['response_dict']['msg']=="文本内没有敏感词":
            positions = positions_all_line_re
            positions_dict_sensitive = positions_dict_sensitive_all_line_re
            word_dict = user_word.find_word_position_regex(text, word_list)  # 用户自定义词组
            word_positions = word_dict['positions']
            word_positions_dict = word_dict['positions_dict']
        else:
            positions=sensitive_dict['positions']+positions_all_line_re #从此开始改变，直到合并字典
            positions = list(set(positions))
            positions_dict_sensitive=sensitive_dict['positions_dict']
            positions_dict_sensitive.update(positions_dict_sensitive_all_line_re)
            word_dict=user_word.find_word_position_regex(text, word_list) # 用户自定义词组
            word_positions=word_dict['positions']
            word_positions_dict=word_dict['positions_dict']
        if positions!='no'and positions!=[]:
            positions=positions+word_positions
            positions = list(set(positions))# 去除重复项
        elif word_positions:
            positions=word_positions
        print("所有敏感词位置", positions)
        one_line_all_char_position = []
        if positions!='no':
            positions_dict = defaultdict(list)
            for d in (positions_dict_sensitive, word_positions_dict):
                for key, value in d.items():
                    positions_dict[key].append(value)
            positions_dict=dict(positions_dict) # 合并字典
            positions_dict = {key: value[0] for key, value in positions_dict.items()}
        # print("所有敏感词位置",positions)
        # one_line_all_char_position=[]
        # if positions!='no':
            for i in positions:
                all_char_location.append(chars[int(i)])
            for characters, positions_characters in positions_dict.items():
                if positions_characters:
                    result_location = [chars[i] for i in positions_characters]
                    #print(positions)
                    print("词组“{}”对应的元素：{}".format(characters, result_location))
                    characters_result_location = dict(characters=characters, result_location=result_location)
                    one_line_all_char_position.append(characters_result_location)
                else:
                    characters=[ ]
                    result_location=[]
                    print("词组“{}”对应的元素：空列表".format(characters))
                # characters_result_location = dict(characters=characters,result_location=result_location)
                # one_line_all_char_position.append(characters_result_location)
        one_line_position = dict(text=text, positions=positions,one_line_all_char_position=one_line_all_char_position)
        all_line_position.append(one_line_position)
    #print(all_char_location)
    result_dict = dict(len_words_result=len_words_result, all_line_position=all_line_position,all_char_location=all_char_location)
    print(result_dict)
    return result_dict

async def use_image_base64_baidu_async(image_base64):
    text_dict=await  picture_async.base64_baidu_async(image_base64)
    words_result = text_dict['words_result']  # words_result
    words_result_num = text_dict['words_result_num']  # words_result_num
    log_id = text_dict['log_id']  # log_id
    all_line_position=[]
    len_words_result=0
    all_char_location=[]
    for i in range(len(words_result)):
        len_words_result=len_words_result+1
        text=words_result[i]['words']  # 对每个成员进行操作
        chars=words_result[i]['chars']
        print("待检测语句",text)
        sensitive_dict = await sensitive_async.sensitive_ai_async(text)
        positions=sensitive_dict['positions']
        positions_dict=sensitive_dict['positions_dict']
        print("所有敏感词位置",positions)
        one_line_all_char_position=[]
        if positions!='no':
            for i in positions:
                all_char_location.append(chars[int(i)])
            for characters, positions_characters in positions_dict.items():
                if positions_characters:
                    result_location = [chars[i] for i in positions_characters]
                    #print(positions)
                    print("词组“{}”对应的元素：{}".format(characters, result_location))
                else:
                    characters=[]
                    result_location=[]
                    print("词组“{}”对应的元素：空列表".format(characters))
                characters_result_location = dict(characters=characters,result_location=result_location)
                one_line_all_char_position.append(characters_result_location)
        one_line_position = dict(text=text, positions=positions,one_line_all_char_position=one_line_all_char_position)
        all_line_position.append(one_line_position)
    #print(all_char_location)
    result_dict = dict(len_words_result=len_words_result, all_line_position=all_line_position,all_char_location=all_char_location)
    print(result_dict)
    return result_dict

# 用百度url的主函数,废弃废弃废弃
async def use_image_base64_word_baidu_async(image_base64,word_list):
    text_dict=await  picture_async.base64_baidu_async(image_base64)
    words_result = text_dict['words_result']  # words_result
    words_result_num = text_dict['words_result_num']  # words_result_num
    log_id = text_dict['log_id']  # log_id
    all_line_position=[]
    len_words_result=0
    all_char_location=[]
    for i in range(len(words_result)):
        len_words_result=len_words_result+1
        text=words_result[i]['words']  # 对每个成员进行操作
        chars=words_result[i]['chars']
        print("待检测语句",text)
        if(i>0):                               # 调用百度的修改，有三行
            time.sleep(1)
        sensitive_dict = await sensitive_async.sensitive_ai_baidu_async(text)
        positions=sensitive_dict['positions'] #从此开始改变，直到合并字典
        positions_dict_sensitive=sensitive_dict['positions_dict']
        word_dict=user_word.find_word_position_regex(text, word_list) # 用户自定义词组
        word_positions=word_dict['positions']
        word_positions_dict=word_dict['positions_dict']
        if positions!='no':
            positions=positions+word_positions
            positions = list(set(positions))# 去除重复项
        elif word_positions:
            positions=word_positions
        print("所有敏感词位置", positions)
        one_line_all_char_position = []
        if positions!='no':
            positions_dict = defaultdict(list)
            for d in (positions_dict_sensitive, word_positions_dict):
                for key, value in d.items():
                    positions_dict[key].append(value)
            positions_dict=dict(positions_dict) # 合并字典
            positions_dict = {key: value[0] for key, value in positions_dict.items()}
        # print("所有敏感词位置",positions)
        # one_line_all_char_position=[]
        # if positions!='no':
            for i in positions:
                all_char_location.append(chars[int(i)])
            for characters, positions_characters in positions_dict.items():
                if positions_characters:
                    result_location = [chars[i] for i in positions_characters]
                    #print(positions)
                    print("词组“{}”对应的元素：{}".format(characters, result_location))
                else:
                    characters=[]
                    result_location=[]
                    print("词组“{}”对应的元素：空列表".format(characters))
                characters_result_location = dict(characters=characters,result_location=result_location)
                one_line_all_char_position.append(characters_result_location)
        one_line_position = dict(text=text, positions=positions,one_line_all_char_position=one_line_all_char_position)
        all_line_position.append(one_line_position)
    #print(all_char_location)
    result_dict = dict(len_words_result=len_words_result, all_line_position=all_line_position,all_char_location=all_char_location)
    print(result_dict)
    return result_dict
# 尝试只调用一次百度敏感词的主函数  base64  *********
async def use_image_base64_word_baidu_async_one(image_base64,word_list):
    text_dict=await  picture_async.base64_baidu_async(image_base64)
    print(text_dict)
    if text_dict['words_result']==[]:
        result_dict = dict(len_words_result=-1, all_line_position=-1, all_char_location=-1)
        print(result_dict)
        return result_dict
    words_result = text_dict['words_result']  # words_result
    words_result_num = text_dict['words_result_num']  # words_result_num
    log_id = text_dict['log_id']  # log_id
    all_line_position=[]
    len_words_result=0
    all_char_location=[]
    all_text=""
    all_line_num_word=[] #从1开始
    res_lines=[]
    for i in range(len(words_result)):
        text = words_result[i]['words']  # 对每个成员进行操作
        line_word_num=len(text)
        all_line_num_word.append(line_word_num)
        all_text=all_text+text
    sensitive_dict = await sensitive_async.sensitive_ai_baidu_async(all_text)
    positions_all_line_re,positions_dict_sensitive_all_line_re=user_word.find_re([],[],all_text)
    print(sensitive_dict)
    positions_new=[]
    positions_dict_new=[]
    if sensitive_dict['response_dict']['conclusion']=='合规':
        if positions_all_line_re!=[] and positions_dict_sensitive_all_line_re!={}:
            positions_all_line=positions_all_line_re
            positions_dict_sensitive_all_line=positions_dict_sensitive_all_line_re
            positions_new = user_word.find_position(positions_all_line, all_line_num_word)
            positions_dict_new = user_word.find_position_dict(positions_dict_sensitive_all_line, all_line_num_word)
        else:
            for i in range(len(words_result)):
                positions_new.append([])
                positions_dict_new.append({})
    else:
        positions_all_line = sensitive_dict['positions']
        positions_dict_sensitive_all_line = sensitive_dict['positions_dict']
        positions_all_line=positions_all_line+positions_all_line_re ##
        positions_all_line = list(set(positions_all_line))
        positions_dict_sensitive_all_line.update(positions_dict_sensitive_all_line_re) ##
        positions_new=user_word.find_position(positions_all_line,all_line_num_word)
        positions_dict_new=user_word.find_position_dict(positions_dict_sensitive_all_line,all_line_num_word)
    for i in range(len(words_result)):
        len_words_result=len_words_result+1
        text=words_result[i]['words']  # 对每个成员进行操作
        chars=words_result[i]['chars']
        print("待检测语句",text)
        # if(i>1):                               # 调用百度的修改，有三行
        #     time.sleep(1)
        # sensitive_dict = await sensitive_async.sensitive_ai_baidu_async(text)
        positions=positions_new[i] #从此开始改变，直到合并字典
        positions_dict_sensitive=positions_dict_new[i]
        word_dict=user_word.find_word_position_regex(text, word_list) # 用户自定义词组
        word_positions=word_dict['positions']
        word_positions_dict=word_dict['positions_dict']
        if positions!='no' and positions!=[]:
            positions=positions+word_positions
            positions = list(set(positions))# 去除重复项
        elif word_positions:
            positions=word_positions
        print("所有敏感词位置", positions)
        one_line_all_char_position = []
        if positions!='no'and positions!=[]:
            positions_dict = defaultdict(list)
            for d in (positions_dict_sensitive, word_positions_dict):
                for key, value in d.items():
                    positions_dict[key].append(value)
            positions_dict=dict(positions_dict) # 合并字典
            positions_dict = {key: value[0] for key, value in positions_dict.items()}
        # print("所有敏感词位置",positions)
        # one_line_all_char_position=[]
        # if positions!='no':
            for i in positions:
                all_char_location.append(chars[int(i)])
            for characters, positions_characters in positions_dict.items():
                if positions_characters:
                    result_location = [chars[i] for i in positions_characters]
                    #print(positions)
                    print("词组“{}”对应的元素：{}".format(characters, result_location))
                else:
                    characters=[]
                    result_location=[]
                    print("词组“{}”对应的元素：空列表".format(characters))
                characters_result_location = dict(characters=characters,result_location=result_location)
                one_line_all_char_position.append(characters_result_location)
        one_line_position = dict(text=text, positions=positions,one_line_all_char_position=one_line_all_char_position)
        all_line_position.append(one_line_position)
    #print(all_char_location)
    result_dict = dict(len_words_result=len_words_result, all_line_position=all_line_position,all_char_location=all_char_location)
    print(result_dict)
    return result_dict
# 尝试只调用一次百度敏感词的主函数  url图片  ************
async def use_image_url_word_baidu_async_one(image_url,word_list):
    text_dict = await picture_async.url_baidu_async(image_url)
    words_result = text_dict['words_result']  # words_result
    words_result_num = text_dict['words_result_num']  # words_result_num
    log_id = text_dict['log_id']  # log_id
    all_line_position = []
    len_words_result = 0
    all_char_location = []
    all_text = ""
    all_line_num_word = []  # 从1开始
    res_lines = []
    for i in range(len(words_result)):
        text = words_result[i]['words']  # 对每个成员进行操作
        line_word_num = len(text)
        all_line_num_word.append(line_word_num)
        all_text = all_text + text
    sensitive_dict = await sensitive_async.sensitive_ai_baidu_async(all_text)
    positions_all_line = sensitive_dict['positions']
    positions_dict_sensitive_all_line = sensitive_dict['positions_dict']
    positions_new = user_word.find_position(positions_all_line, all_line_num_word)
    positions_dict_new = user_word.find_position_dict(positions_dict_sensitive_all_line, all_line_num_word)
    for i in range(len(words_result)):
        len_words_result = len_words_result + 1
        text = words_result[i]['words']  # 对每个成员进行操作
        chars = words_result[i]['chars']
        print("待检测语句", text)
        # if(i>1):                               # 调用百度的修改，有三行
        #     time.sleep(1)
        # sensitive_dict = await sensitive_async.sensitive_ai_baidu_async(text)
        positions = positions_new[i]  # 从此开始改变，直到合并字典
        positions_dict_sensitive = positions_dict_new[i]
        word_dict = user_word.find_word_position_regex(text, word_list)  # 用户自定义词组
        word_positions = word_dict['positions']
        word_positions_dict = word_dict['positions_dict']
        if positions != 'no' and positions != []:
            positions = positions + word_positions
            positions = list(set(positions))  # 去除重复项
        elif word_positions:
            positions = word_positions
        print("所有敏感词位置", positions)
        one_line_all_char_position = []
        if positions != 'no' and positions != []:
            positions_dict = defaultdict(list)
            for d in (positions_dict_sensitive, word_positions_dict):
                for key, value in d.items():
                    positions_dict[key].append(value)
            positions_dict = dict(positions_dict)  # 合并字典
            positions_dict = {key: value[0] for key, value in positions_dict.items()}
            # print("所有敏感词位置",positions)
            # one_line_all_char_position=[]
            # if positions!='no':
            for i in positions:
                all_char_location.append(chars[int(i)])
            for characters, positions_characters in positions_dict.items():
                if positions_characters:
                    result_location = [chars[i] for i in positions_characters]
                    # print(positions)
                    print("词组“{}”对应的元素：{}".format(characters, result_location))
                else:
                    characters = []
                    result_location = []
                    print("词组“{}”对应的元素：空列表".format(characters))
                characters_result_location = dict(characters=characters, result_location=result_location)
                one_line_all_char_position.append(characters_result_location)
        one_line_position = dict(text=text, positions=positions, one_line_all_char_position=one_line_all_char_position)
        all_line_position.append(one_line_position)
    # print(all_char_location)
    result_dict = dict(len_words_result=len_words_result, all_line_position=all_line_position,
                       all_char_location=all_char_location)
    print(result_dict)
    return result_dict

if __name__ == '__main__':
    # image_url = "http://dl2.iteye.com/upload/attachment/0129/4482/19f369de-84a5-3813-b220-86a27b950837.png"
    # use_image_url(image_url)
    # base64='data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAOIAAADYCAYAAAD28T8cAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAAEnQAABJ0Ad5mH3gAAAJvSURBVHhe7dMxAQAwDMCg+ffbu5PRHBxI4M3MArdEhAARIUBECBARAkSEABEhQEQIEBECRIQAESFARAgQEQJEhAARIUBECBARAkSEABEhQEQIEBECRIQAESFARAgQEQJEhAARIUBECBARAkSEABEhQEQIEBECRIQAESFARAgQEQJEhAARIUBECBARAkSEABEhQEQIEBECRIQAESFARAgQEQJEhAARIUBECBARAkSEABEhQEQIEBECRIQAESFARAgQEQJEhAARIUBECBARAkSEABEhQEQIEBECRIQAESFARAgQEQJEhAARIUBECBARAkSEABEhQEQIEBECRIQAESFARAgQEQJEhAARIUBECBARAkSEABEhQEQIEBECRIQAESFARAgQEQJEhAARIUBECBARAkSEABEhQEQIEBECRIQAESFARAgQEQJEhAARIUBECBARAkSEABEhQEQIEBECRIQAESFARAgQEQJEhAARIUBECBARAkSEABEhQEQIEBECRIQAESFARAgQEQJEhAARIUBECBARAkSEABEhQEQIEBECRIQAESFARAgQEQJEhAARIUBECBARAkSEABEhQEQIEBECRIQAESFARAgQEQJEhAARIUBECBARAkSEABEhQEQIEBECRIQAESFARAgQEQJEhAARIUBECBARAkSEABEhQEQIEBECRIQAESFARAgQEQJEhAARIUBECBARAkSEABEhQEQIEBECRIQAESFARAgQEQJEhAARIUBECBARAkSEABEhQEQIEBECRIQAESFARAgQEQJEhAARIUBECBARAkSEABEhQEQIEBECRIQAESFARDg3+wEfn5fQbUrDFwAAAABJRU5ErkJggg=='
    # base64='data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADsAAAAlCAYAAAD8+ZFYAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAAEnQAABJ0Ad5mH3gAAAIASURBVGhD7ZihTgNBEIb7Ln0AFAQJogmSBAOuSBL6ABA8toaAhQpEDQ4DCHB4XgCFOLgKTh/5m/zNdDJ77e1ewt3eiS9ldmeX+Xb22rS9m2SUXyUnUfPwM86zLMt71mSMfP1+tkf2ffbYHtnXdNrJRkknGyudbKy0SvZtVoHs1mAjPzjbWcTH47283+8v5bi4/BjOc89fDs35KnlOJ2GyVrFavgisw3rso8dWMbrfX9prFZPvizBZdHEw3F7EKACFyOKLQD4Ox5qz4OGWWUOuk9MwWfxTecKI5em74Bp9WEWw4z6ixFuWXXTFFix492hz/mph3QruHSIKvGXZRfzN6yW7bD2P6KJ8nuXNsPJlXqgo8JLlSVMWsb6OunjGeEXMA+I89+R6CURx5a25MnjJoijIuYoDRZ3ivOwWZFzd+zdZXEOIWp3gGASlrO4q0G9O2BdADLnrwLXrUlqWp2/JYo7PpO4s5qSc7hZi7MlYonN98X6D0rJaTsfMZ3dRPNfrXE3tZNE12TlLQHeXOUCOa2oly6LZNTkmZbnGGpMfSZpayequAksWYEwWzhivkJK5pHbXWOOSlehD0tdcjtdadtU8pFyd1GAf7GfNlaFSWV5H4uoGxq0OEt4KUpS7LsHfeprEbej32SbxlN61R7aS36CaQvdTaqx0srHSMtlp/gcCINunAzkYDAAAAABJRU5ErkJggg=='
    # base64='data:image/png;base64,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'
    # base64='data:image/png;base64,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'
    base64 = 'data:image/png;base64,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'
    loop = asyncio.get_event_loop()
    # result_dict = loop.run_until_complete(use_image_base64_async(base64))
    wordlist = ["好", "dog"]
    result_dict = loop.run_until_complete(use_image_base64_word_baidu_async_one(base64, wordlist))
    # result_dict = loop.run_until_complete(use_image_base64_word_baidu_async_one(base64,wordlist))
    print(result_dict)
