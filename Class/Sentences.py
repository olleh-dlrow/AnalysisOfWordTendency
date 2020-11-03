# 获取积极情感句子，返回列表
def get_pos_sentences(filename):
    sentences = []
    with open("../Sources/" + filename, "r", encoding="UTF-8") as f:
        for line in f:
            if line[0] == '1':
                sentences.append(line[2:])
            else:
                break
    f.close()
    return sentences


# 获取消极情感句子，返回列表
def get_neg_sentences(filename):
    sentences = []
    with open("../Sources/" + filename, "r", encoding="UTF-8") as f:
        for line in f:
            if line[0] == '0':
                sentences.append(line[2:])
            else:
                break
    f.close()
    return sentences


# 将句子写入文件中
def write_sen_to_file(sentences, filename):
    with open("../Sources/" + filename, "w", encoding="UTF-8") as wf:
        for sentence in sentences:
            wf.write(sentence)
    wf.close()
