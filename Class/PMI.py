from cmath import log


# 计算情感词和种子词的PMI，需要他们各自的频率和共现的频率
def get_PMI(word, seed_word, all_concur_freqs, word_freq, seed_freqs):
    result = (all_concur_freqs[seed_word][word] + 1) / (word_freq * seed_freqs[seed_word] + 1)
    return log(result, 2)


# 利用所有种子词计算某个情感词的情感倾向
def get_SO_PMI(word, all_concur_freqs_dict, word_freq, seed_freqs_dict):
    all_concur_pos_freqs = all_concur_freqs_dict['pos']
    all_concur_neg_freqs = all_concur_freqs_dict['neg']
    pos_seed_freqs = seed_freqs_dict['pos']
    neg_seed_freqs = seed_freqs_dict['neg']
    pos_PMI = 0
    neg_PMI = 0
    for pos_seed in pos_seed_freqs.keys():
        pos_PMI += get_PMI(word, pos_seed, all_concur_pos_freqs, word_freq, pos_seed_freqs)
    for neg_seed in neg_seed_freqs.keys():
        neg_PMI += get_PMI(word, neg_seed, all_concur_neg_freqs, word_freq, neg_seed_freqs)

    result = pos_PMI - neg_PMI
    return result


# 获得word_freqs中所有词的SO_PMI值，正向情感词和负向情感词要分开计算SO_PMI
def get_all_words_SO_PMI(word_freqs, all_concur_freqs_dict, seed_freqs_dict):
    SO_PMI_dict = {}
    word_list = word_freqs.keys()
    for word in word_list:
        SO_PMI = get_SO_PMI(word, all_concur_freqs_dict, word_freqs[word], seed_freqs_dict)
        SO_PMI_dict[word] = SO_PMI.real
    return SO_PMI_dict


# 将SO_PMI输出到文件中
def write_SO_PMIs_to_file(SO_PMI_dict, filename, rev):
    with open("../Sources/" + filename, "w", encoding="UTF-8") as f:
        li = sorted(SO_PMI_dict.items(), key=lambda kv: kv[1], reverse=rev)
        for i in range(0, 50):
            item = li[i]
            key = item[0]
            val = item[1]
            f.write(str(key) + ":" + str(val) + "\n")
    f.close()
