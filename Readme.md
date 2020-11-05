# 外卖评论情感分析

基于无监督学习方法判断新词的语义倾向性。

编程语言：Python

使用分词库：jiagu

## 算法核心

选取一系列的正向和负向种子词，根据PMI-SO方法计算新词与正向种子词的点态互信息之和，再减去该词与负向种子词的点态互信息之和。

两个词的点态互信息（PMI）为：
$$
PMI(word_1, word_2) = log_2(\frac{P(word_{1}\cap word_{2})}{P(word_1)P(word_2)})
$$
其中$P(word_1 \cap word_2)$表示$word_1$与$word_2$在文档集中共同出现的概率。

新词的语义倾向值的计算公式为：
$$
SO-PMI(word) = \sum_{pword\in{Pwords}}PMI(word, pword) - \sum_{nword\in Nwords}PMI(word, nword)
$$
其中，Pwords为正向种子词的集合，Nwords为负向种子词的集合。

> 在实际处理的过程中，由于log的自变量不能为0，所以可以对分子和分母增加偏移量来避免出现log(0)的情形。

## 主要功能

根据词性将词语归类

```python
# 分词 类
class Words:
    	...
   def __init__(self, sen):
        self.sentence = sen                            # 原始句子
        self.words_list = jiagu.seg(sen)               # 分词结果列表：保存每个词语的相对位置
        self.words_dict = {}                           # 词性-词语列表 字典：通过词性来查找到相应的词语
        self.word_class_dict = {}                      # 词语-词性字典：通过词语来找到其对应的词性
        self.word_pos_dict = {}                        # 词语-位置索引字典：通过词语找到其在分词列表中的位置
       
        word_class_list = jiagu.pos(self.words_list)   # 获取每个词的词性
        # 将词性和词语关联起来放到字典中
        word_class_set = set(word_class_list)          # 获取词性的集合作为字典的键值
        for word_class in word_class_set:
            self.words_dict[word_class] = []
        for index in range(0, len(self.words_list)):
            self.words_dict[word_class_list[index]].append(self.words_list[index])
            self.word_class_dict[self.words_list[index]] = word_class_list[index]
            self.word_pos_dict[self.words_list[index]] = index    
```

由于情感词往往会跟上一些形容词或者副词在前面修饰，情感词所表达的情感倾向会受到很大的影响，如果跟上一些否定词语，结果会大相径庭，因此需要根据词语的位置和词性对分词进行重组。

```python
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
```

其他功能的函数：

句子处理：

```python
# 获取积极情感句子，返回列表
def get_pos_sentences(filename)

# 获取消极情感句子，返回列表
def get_neg_sentences(filename)

# 将句子写入文件中
def write_sen_to_file(sentences, filename)
```

Words类的处理:

```python
# 将文件中的句子拆分成Words对象
def get_words(filename)

# 获取Words中所有形容词（情感词）出现的频率，储存到字典中
def get_freqs(words_list)
```

种子词处理：

```python
# 选取情感情感种子词
def get_seeds(filename)

# 获取种子词的频率
def get_seed_freqs(seed_list, words_list)
```

共现频率处理：

```python
# 获取所有种子词和所有情感词共现的频率，用二维词典存储，freqs[seed][adj_word]
def get_all_concur_freqs(seeds, words_list)

# 获取指定种子词和所有情感词共现的频率
def get_concur_freqs(seed_word, words_list)
```

计算PMI：

```python
# 计算情感词和种子词的PMI，需要他们各自的频率和共现的频率
def get_PMI(word, seed_word, all_concur_freqs, word_freq, seed_freqs)

# 利用所有种子词计算某个情感词的情感倾向
def get_SO_PMI(word, all_concur_freqs_dict, word_freq, seed_freqs_dict)

# 获得word_freqs中所有词的SO_PMI值，正向情感词和负向情感词要分开计算SO_PMI
def get_all_words_SO_PMI(word_freqs, all_concur_freqs_dict, seed_freqs_dict)

# 将SO_PMI输出到文件中
def write_SO_PMIs_to_file(SO_PMI_dict, filename, rev)
```

## 注意问题

1. 种子词的选取需要恰当，种子词的数量和出现频率会大大影响结果。
2. 由于评论的成分会比较复杂，许多评论既有正向的情感倾向，又有负向的情感倾向，因此最终结果中会有部分意想不到的词语出现（比如一个PMI-SO值很低的正向词）。
3. 计算公式中如果使用偏移量，可能会影响部分词语的绝对值，但是总体情感倾向排名不会有太大变化。