import pandas as pd

# df = pd.read_csv('./crawling_data/reviews_2020_1.csv', index_col=0)
# df.to_csv('./crawling_data/reviews_2020_1.csv', index=False)

# df = pd.read_csv('./crawling_data/reviews_2020_1.csv')
# df.info()
# df = pd.DataFrame()
# for i in range(1, 38):
#     df_temp = pd.read_csv(
#         './crawling_data/reviews_2020_{}.csv'.format(i))
#     df_temp.dropna(inplace=True)
#     df_temp.drop_duplicates(inplace=True)
#     df_temp.columns = ['title','reviews']
#     df_temp.to_csv('./crawling_data/reviews_2020_{}.csv'.format(i),
#                    index=False)
#     df = pd.concat([df, df_temp], ignore_index=True)
# df.info()
# df.to_csv('./crawling_data/reviews_2020.csv', index=False)

df = pd.DataFrame()
for i in range(15, 22):
    df_temp = pd.read_csv(
        './crawling_data/reviews_20{}.csv'.format(i))
    df_temp.dropna(inplace=True)
    df_temp.drop_duplicates(inplace=True)
    df_temp.columns = ['title','reviews']
    df_temp.to_csv('./crawling_data/reviews_20{}.csv'.format(i),
                   index=False)
    df = pd.concat([df, df_temp], ignore_index=True)
df.drop_duplicates(inplace=True)
df.info()
df.to_csv('./crawling_data/naver_movie_reviews_2015_2021.csv', index=False)




