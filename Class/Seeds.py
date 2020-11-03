# 选取5个情感情感种子词
def get_seeds(filename):
    seeds = []
    with open("../Sources/" + filename, "r", encoding="UTF-8") as f:
        for line in f:
            line = line.replace("\n", "")
            seeds.append(line)
    return seeds


# 获取种子词的频率
def get_seed_freqs(seed_list, words_list):
    seed_freqs = {}
    for seed in seed_list:
        for words in words_list:
            sentence = words.sentence
            if seed in sentence:
                if seed not in seed_freqs.keys():
                    seed_freqs[seed] = 1
                else:
                    seed_freqs[seed] += 1
    return seed_freqs
