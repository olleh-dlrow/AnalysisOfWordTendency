# 获取所有种子词和所有情感词共现的频率，用二维词典存储，freqs[seed][adj_word]
def get_all_concur_freqs(seeds, words_list):
    all_concur_freqs = {}
    for seed in seeds:
        all_concur_freqs[seed] = get_concur_freqs(seed, words_list)
    return all_concur_freqs


# 获取指定种子词和所有情感词共现的频率
def get_concur_freqs(seed_word, words_list):
    concur_freqs = {}
    for words in words_list:
        sentence = words.sentence
        if 'a' in words.words_dict.keys():
            adj_word_list = words.words_dict['a']
            for adj_word in adj_word_list:
                concur_freqs[adj_word] = 0
                if seed_word in sentence:
                    if adj_word not in concur_freqs.keys():
                        concur_freqs[adj_word] = 1
                    else:
                        concur_freqs[adj_word] += 1

    return concur_freqs