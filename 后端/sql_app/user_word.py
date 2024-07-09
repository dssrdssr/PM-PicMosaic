import re

def find_position(all_words, num_word_of_line):
    res_list=[]
    total_chars = sum(num_word_of_line)  # 获取所有行的字符总数
    if all_words[-1] > total_chars:  # 检查最后一个位置是否超出总字符数
        return "位置超出总字符数"
    else:
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
                        print( f"位置{item}来自第{line_number}行的第{char_position}个字符")
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
            print(f"词语'{word}'在句子中的位置是{position_word}个字符")
        if not position_word:
            print(f"句子中不存在词语'{word}'")
        positions_dict[word] = position_word
    # print(positions)
    # print(positions_dict)
    result_dict = dict(response_dict="find_word_position_regex", positions=positions, positions_dict=positions_dict)
    return result_dict
# 测试示例
if __name__ == '__main__':
    sentence = "我喜欢香蕉吃苹果和香蕉"
    word_list = ["香蕉", "橙子"]
    find_word_position_regex(sentence, word_list)