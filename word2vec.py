import pandas as pd
from gensim.models import Word2Vec

review_word = pd.read_csv('./crawling_data/cleaned_review_2015_2021.csv')
review_word.info()
#print(review_word.head())

cleaned_token_review = list(review_word['cleaned_sentences'])

print(cleaned_token_review[0])
exit()

cleaned_tokens = []
for sentence in cleaned_token_review:
    token = sentence.split()
    cleaned_tokens.append(token)
#print(cleaned_tokens)
embedding_model = Word2Vec(cleaned_tokens, size=100,
            window=4, min_count=20,
            workers=4, iter=100, sg=1)   # gensim 4.0.0 size => vector_size, iter => epochs
embedding_model.save('./models/word2VecModel_2015_2021.model')
print(embedding_model.wv.vocab.keys())      # print(list(embedding_model.wv.index_to_key))
print(len(embedding_model.wv.vocab.keys())) # print(len(list(embedding_model.wv.index_to_key)))













