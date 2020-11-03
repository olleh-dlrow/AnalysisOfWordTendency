import jiagu


# 基本数据成员：
# 原始句子
# 词性-词语列表 字典：通过词性来查找到相应的词语
# 分词结果列表：保存每个词语的相对位置
# 词语-词性字典：通过词语来找到其对应的词性
# 词语-位置索引字典：通过词语找到其在分词列表中的位置
class Words:

    def __init__(self, sen):
        self.sentence = sen
        self.words_list = jiagu.seg(sen)
        self.words_dict = {}
        self.word_class_dict = {}
        self.word_pos_dict = {}

        # 获取每个词的词性
        word_class_list = jiagu.pos(self.words_list)
        # 将词性和词语关联起来放到字典中
        word_class_set = set(word_class_list)  # 获取词性的集合作为字典的键值
        for word_class in word_class_set:
            self.words_dict[word_class] = []
        for index in range(0, len(self.words_list)):
            self.words_dict[word_class_list[index]].append(self.words_list[index])
            self.word_class_dict[self.words_list[index]] = word_class_list[index]
            self.word_pos_dict[self.words_list[index]] = index

    # 将所有内容转换成字符串，便于显示和输出
    def to_string(self):
        result = ''
        result += '原始句子：' + self.sentence + '\n'
        result += '分词结果：\n'
        result += '[' + ','.join(self.words_list) + ']\n'
        result += '词性-词语字典：\n'
        for word_class, words in self.words_dict.items():
            result += word_class + ':[' + ','.join(words) + ']\n'

        result += '词语-词性字典：\n'
        result += str(self.word_class_dict) + '\n'
        return result

    # 根据词语的位置和前后词语的词性来生成新词,并在words_dict词典中删除原来的词语
    def get_new_words(self):
        if 'a' not in self.words_dict.keys():
            return
        adj_words_list = self.words_dict['a'].copy()
        for word in adj_words_list:
            index = self.word_pos_dict[word]
            pre_index = index - 1
            if pre_index >= 0:
                pre_word = self.words_list[pre_index]
                if self.word_class_dict[pre_word] == 'd':
                    new_word = pre_word + word
                    self.words_dict['a'].append(new_word)
                    self.words_dict['a'].remove(word)


# 将文件中的句子拆分成Words对象
def get_words(filename):
    words_list = []
    with open("../Sources/" + filename, "r", encoding="UTF-8") as f:
        for line in f:
            line = line.replace("\n", "")
            words = Words(line)
            words.get_new_words()
            words_list.append(words)
    f.close()
    return words_list


# 获取Words中所有形容词（情感词）出现的频率，储存到字典中
def get_freqs(words_list):
    freqs_dict = {}
    for words in words_list:
        words_dict = words.words_dict
        if 'a' in words_dict.keys():
            for adj_word in words_dict['a']:
                if adj_word not in freqs_dict.keys():
                    freqs_dict[adj_word] = 1
                else:
                    freqs_dict[adj_word] += 1
    return freqs_dict
