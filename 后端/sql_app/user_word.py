import re

def find_position(all_words, num_word_of_line):
    res_list=[]
    total_chars = sum(num_word_of_line)  # 获取所有行的字符总数
    # if all_words[-1] > total_chars:  # 检查最后一个位置是否超出总字符数
    #     return "位置超出总字符数"
    # else:
    total = 0
    for i, chars in enumerate(num_word_of_line):
        line_list=[]
        total += chars
        for item in all_words:
            if item <= total-1:
                line_number = i + 1  # 确定P中文字来自第几行
                char_position = chars - (total - item) + 1  # 确定P中文字在该行的第几个
                if(char_position>0):
                    line_list.append(char_position-1)
    
        res_list.append(line_list)
        dict(line=i,line_list=line_list)
    return res_list

def find_position_dict(all_words_dict,num_word_of_line):
    line_dicts = []
    start = 0
    for c in num_word_of_line:
        end = start + c
        line_dict={}
        for k, v in all_words_dict.items():
            pos_list = []
            for m in v :
                if m in range(start, end):
                    pos_list.append(m-start)
            if pos_list!=[]:
                line_dict[k]=pos_list
        line_dicts.append(line_dict)
        start = end
    return line_dicts
# 句子当中找匹配的词语
def find_word_position_regex(sentence, word_list):
    positions=[]
    positions_dict={}
    for word in word_list:
        position_word=[]
        matches = re.finditer(word, sentence)  # 在句子中寻找匹配的词语
        for match in matches:
            for i in range(len(word)):
                positions.append(match.start() + i)
                position_word.append((match.start() + i))
            # index = match.start() + 1  # 获取词语在句子中的位置（加1是为了转换为从1开始的索引）
            
        positions_dict[word] = position_word
    # print(positions)
    # print(positions_dict)
    result_dict = dict(response_dict="find_word_position_regex", positions=positions, positions_dict=positions_dict)
    return result_dict

#  正则式匹配
def find_re(re_list,re_name_list,text):
    if re_list==[] or re_name_list==[]:
        re_1 = r'([1-9]\d{5}(18|19|20)?\d{2}(0[1-9]|1[0-2])(0[1-9]|[1-2]\d|3[0-1])\d{3}(\d|X|x))'
        re_2 = r'\b\d{12,19}\b'
        re_3 = r'\d{6,6}'
        re_list.append(re_1)
        re_list.append(re_2)
        re_list.append(re_3)
        re_name_1="re身份证号"
        re_name_2 = "re银行卡号"
        re_name_3="re银行卡密码"
        re_name_list.append(re_name_1)
        re_name_list.append(re_name_2)
        re_name_list.append(re_name_3)
    positions = []
    positions_dict={}
    for i in range (len(re_list)):
        regex = re.compile(re_list[i])
        result = regex.finditer(text)
        re_pos=[]
        for match in result:
          
            start, end = match.span()
            positions.extend(range(start, end))
            re_pos.extend(range(start, end))
        re_pos = list(set(re_pos))
        if re_pos!=[]:
            positions_dict[re_name_list[i]]=re_pos
    positions = list(set(positions))
    return positions,positions_dict
    # 测试示例

if __name__ == '__main__':
    re_list=[]
    re_1=r'([1-9]\d{5}(18|19|20)?\d{2}(0[1-9]|1[0-2])(0[1-9]|[1-2]\d|3[0-1])\d{3}(\d|X|x))'
    re_2=r'\b\d{12,19}\b'
    re_list.append(re_1)
    re_list.append(re_2)
    text="aabb"
    #text="#410325199610012345这是一个身份证号码：410325199610012345，和一个银行卡号：6222021234567890123。"
    positions,positions_dict=find_re([],[],text)
  
