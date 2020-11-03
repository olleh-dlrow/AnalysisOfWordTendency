# 从文件中读取句子，将其转换为Words对象
# 获取每个情感形容词的词频，并且生成新词
# 获取情感词
# 计算两个词之间共现的概率（函数）
# 计算PMI
from Class.Words import get_words, get_freqs
from Class.Seeds import get_seeds, get_seed_freqs
from Class.PMI import get_all_words_SO_PMI, write_SO_PMIs_to_file
from Script.concurrence import get_all_concur_freqs

# 从文件中读取句子，并处理成Words对象
print("Getting Words objects from files of sentences...")
words_list_dict = {'pos': get_words("pos_sentences.txt"), 'neg': get_words("neg_sentences.txt")}
print("Generate Words successfully!\n")

# 所有情感词
words_list = words_list_dict['pos'] + words_list_dict['neg']

# 获取情感词的词频
print("Getting emotion words' frequencies from Words...")
word_freqs_dict = {'pos': get_freqs(words_list_dict['pos']), 'neg': get_freqs(words_list_dict['neg'])}
print("Generate emotion words' frequencies successfully!\n")

# 获取种子词
print("Getting emotion seeds from files...")
seed_list_dict = {'pos': get_seeds("pos_seeds.txt"), 'neg': get_seeds("neg_seeds.txt")}
print("Generate emotion seeds successfully!\n")

# 获取种子词的词频
print("Getting seeds' frequencies from seeds and sentences...")
seed_freqs_dict = {'pos': get_seed_freqs(seed_list_dict['pos'], words_list_dict['pos']),
                   'neg': get_seed_freqs(seed_list_dict['neg'], words_list_dict['neg'])}
print("Generate seeds' frequencies successfully!\n")

# 获取种子词和情感词共现的频率
print("Getting frequencies of concurrence between the seed and emotion word from seeds and words...")
all_concur_freqs_dict = {'pos': get_all_concur_freqs(seed_list_dict['pos'], words_list),
                         'neg': get_all_concur_freqs(seed_list_dict['neg'], words_list)}
print("Generate concurrence frequencies successfully!\n")

# 获取正向情感词的情感倾向
print("Getting SO_PMIs of positive words...")
pos_SO_PMI_dict = get_all_words_SO_PMI(word_freqs_dict['pos'], all_concur_freqs_dict, seed_freqs_dict)
print("Generate SO_PMIs of positive words successfully!")
write_SO_PMIs_to_file(pos_SO_PMI_dict, "pos_result.txt", True)
print("SO_PMIs of positive words have been written to " + "pos_result.txt" + " successfully!\n")


# 获取负向情感词的情感倾向
print("Getting SO_PMIs of negative words...")
neg_SO_PMI_dict = get_all_words_SO_PMI(word_freqs_dict['neg'], all_concur_freqs_dict, seed_freqs_dict)
print("Generate SO_PMIs of negative words successfully!")
write_SO_PMIs_to_file(neg_SO_PMI_dict, "neg_result.txt", False)
print("SO_PMIs of negative words have been written to " + "neg_result.txt" + " successfully!\n")
