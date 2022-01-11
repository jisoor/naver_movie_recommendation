import pandas as pd
from sklearn.metrics.pairwise import linear_kernel
from scipy.io import mmwrite, mmread
import pickle
from gensim.models import Word2Vec

def getRecommendation(cosine_sim):
    simScore = list(enumerate(cosine_sim[-1]))
    simScore = sorted(simScore, key=lambda x:x[1],
                      reverse=True)
    simScore = simScore[1:11]
    movieidx = [i[0] for i in simScore]
    recMovieList = df_reviews.iloc[movieidx]
    return recMovieList

df_reviews = pd.read_csv('./crawling_data/cleaned_review_2015_2021.csv')
Tfidf_matrix = mmread('./models/Tfidf_movie_review.mtx').tocsr()
with open('./models/tfidf.pickle', 'rb') as f:
    Tfidf = pickle.load(f)

# # 영화 제목 / index를 이용
# movie_idx = df_reviews[df_reviews['titles']=='겨울왕국 2 (Frozen 2)'].index[0]
# print(movie_idx)
#
# #movie_idx = 10
# print(df_reviews.iloc[movie_idx, 0])
#
# cosine_sim = linear_kernel(Tfidf_matrix[movie_idx],
#                            Tfidf_matrix)
# recommendation = getRecommendation(cosine_sim)
# print(recommendation.iloc[:, 0])

# embedding_model = Word2Vec.load('./models/word2VecModel_2015_2021.model')
#
# key_word = '스파이더맨'
# sentence = [key_word] * 11
# sim_word = embedding_model.wv.most_similar(key_word, topn=10)
# words = []
# for word, _ in sim_word:
#     words.append(word)
# print(words)
# for i, word in enumerate(words):
#     sentence += [word] * (10-i)
# sentence = ' '.join(sentence)
# print(sentence)
# sentence_vec = Tfidf.transform([sentence])
# cosine_sim = linear_kernel(sentence_vec,
#                            Tfidf_matrix)
# recommendation = getRecommendation(cosine_sim)
# print(recommendation['titles'])


sentence ='어느 날 기이한 존재로부터 지옥행을 선고받은 사람들. 충격과 두려움에 휩싸인 도시에 대혼란의 시대가 도래한다. 신의 심판을 외치며 세를 확장하려는 종교단체와 진실을 파헤치는 자들의 이야기.'
sentence_vec = Tfidf.transform([sentence])
cosine_sim = linear_kernel(sentence_vec,
                           Tfidf_matrix)
recommendation = getRecommendation(cosine_sim)
print(recommendation['titles'])
