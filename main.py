import sys

import numpy
import textHandle

if __name__ == "__main__":
    teststring = "复旦大学美国研究中心副主任信强在接受《环球时报》记者采访时表示，拜登上台可能会为中美关系带来一个喘息期。\
他认为，目前中美的摩擦和对立已遍及所有领域，并处在“快速恶性循环”的轨道上，整体表现为三个特征：战略互信的摧毁，高层政治互动几乎停摆，\
没有任何实质合作。拜登上台，至少中美可在后两方面有所突破。预计中美会在疫苗、抗疫、气候变化等领域恢复较为务实的建设性合作，\
一些此前停摆的对话和联络机制也有望恢复。但战略互信的重建，却并非一朝一夕之功。信强分析称。不过，总统的更换或许不会改变华盛顿对华政策的总体方向。\
无论谁入主白宫，美国与中国的关系都将或多或少维持现状，美国CNBC近日援引白宫前首席贸易谈判代表威廉姆斯的话这样预测称。\
对中国强硬是使美国这个两极分化的国家团结起来的原因。我们在政治上是两极化的，但在中国问题上，我们不存在两极化，威廉姆斯说，\
但与特朗普不同的是，拜登的政策可能更稳健，更具可预测性。你不会在半夜发推文宣布关税之类的事情，但总体轨迹将大致相同。\
国际关系学院校长助理、国际政治系主任达巍告诉《环球时报》记者，拜登的对华政策不会简单地回到2016年“奥巴马时代”，因为过去四年间，\
中美关系和世界都已发生巨大改变，两国精英和民众对对方的看法也几乎彻底重塑。拜登对中国政策的调整，势必将建立在特朗普时代的基础之上——事实上，\
对华政策的彻底改变，可能正是特朗普政府留给美国最大的政治遗产。达巍认为。他表示，对华接触政策需要调整已渐成美国朝野的共识，\
拜登上台也难改两国走向竞争与对抗的大趋势，问题是他将出台怎样的替代性政策框架尚不清楚。不过，竞争并不意味着脱钩。我不认为拜登政府会赞成对华全面脱钩战略。"

    if len(sys.argv) == 1:
        ustring = teststring
    else:
        ustring = sys.argv[1]

    # 1. cut sentence
    sentences = textHandle.cut_sent(ustring)
    # 2. cut words
    words = textHandle.cut_word(ustring)
    # 3. find the most frequent words
    top_n_words = textHandle.top_n_words(words, 6)
    # 4. score sentences
    s = [s[0] for s in top_n_words]
    scored_sentences = textHandle.score_sentences(sentences, s)
    # Summaization Approach 1:
    # Filter out non-significant sentences by using the average score plus a
    # fraction of the std dev as a filter

    avg = numpy.mean([s[1] for s in scored_sentences])
    std = numpy.std([s[1] for s in scored_sentences])
    mean_scored = [(sent_idx, score) for (sent_idx, score) in scored_sentences
                   if score > avg + 0.5 * std]

    # Summarization Approach 2:
    # Another approach would be to return only the top N ranked sentences

    top_n_scored = sorted(scored_sentences, key=lambda s: s[1])[-5:]
    top_n_scored = sorted(top_n_scored, key=lambda s: s[0])

    # Decorate the post object with summaries
    print(top_n_scored)
    d = dict(top_n_summary=[sentences[idx] for (idx, score) in top_n_scored],
             mean_scored_summary=[sentences[idx] for (idx, score) in mean_scored])
    print(d['top_n_summary'])
    print(d['mean_scored_summary'])

