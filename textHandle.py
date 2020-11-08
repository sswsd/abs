import re
import jieba


def cut_sent(text):
    text = re.sub('([。！？\?])([^”’])', r"\1\n\2", text)  # 单字符断句符
    para = re.sub('(\.{6})([^”’])', r"\1\n\2", text)  # 英文省略号
    para = re.sub('(\…{2})([^”’])', r"\1\n\2", text)  # 中文省略号
    para = re.sub('([。！？\?][”’])([^，。！？\?])', r'\1\n\2', text)

    # 如果双引号前有终止符，那么双引号才是句子的终点，把分句符\n放到双引号后，注意前面的几句都小心保留了双引号
    text = text.rstrip()  # 段尾如果有多余的\n就去掉它
    # 很多规则中会考虑分号;，但是这里我把它忽略不计，破折号、英文双引号等同样忽略，需要的再做些简单调整即可。
    return text.split("\n")


def cut_word(text):
    words = jieba.lcut_for_search(text)
    return words


def top_n_words(words, n):
    counts = {}  # 通过键值对的形式存储词语及其出现的次数
    for word in words:
        if len(word) == 1:
            continue
        else:
            counts[word] = counts.get(word, 0) + 1
    items = list(counts.items())
    items.sort(key=lambda x: x[1], reverse=True)
    top_words = items[0:n]
    return top_words


def score_sentences(sentences, top_n_words):
    scores = []
    sentence_idx = -1

    for s in [cut_word(s) for s in sentences]:
        sentence_idx += 1
        word_idx = []

        for word in top_n_words:
            try:
                word_idx.append(s.index(word))
            except ValueError as e:
                pass
        word_idx.sort()

        if len(word_idx) == 0: continue

        # Using the word index, compute clusters by using a max distance threshold
        # for any two consecutive words

        clusters = []
        cluster = [word_idx[0]]
        i = 1
        while i < len(word_idx):
            if word_idx[i] - word_idx[i - 1] < 5:
                cluster.append(word_idx[i])
            else:
                clusters.append(cluster[:])
                cluster = [word_idx[i]]
            i += 1
        clusters.append(cluster)

        # Score each cluster. The max score for any given cluster is the score
        # for the sentence

        max_cluster_score = 0
        for c in clusters:
            significant_words_in_cluster = len(c)
            total_words_in_cluster = c[-1] - c[0] + 1
            score = 1.0 * significant_words_in_cluster \
                    * significant_words_in_cluster / total_words_in_cluster

            if score > max_cluster_score:
                max_cluster_score = score

        scores.append((sentence_idx, score))
    return scores

    # for i in range(20):
    #    word, count = items[i]
    #    print("{0:<5}{1:>5}".format(word, count))
    # print(words2)
    # fdist = nltk.FreqDist(words)
    # fdist = list(fdist.items())
    # fdist.sort(key=lambda x: x[1], reverse=True)
    # for j in range(20):
    #    word, count = fdist[j]
    #    print(word, count)