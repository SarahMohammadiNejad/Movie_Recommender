
import pandas as pd
def read_movie_data():
    df_movies = pd.read_csv("ml-latest-small/movies.csv")
    df_ratings = pd.read_csv("ml-latest-small/ratings.csv")
    # df_tags = pd.read_csv("ml-latest-small/tags.csv")
    # df_links = pd.read_csv("ml-latest-small/links.csv")
    return df_movies, df_ratings

def filter_popular_high_rate(df_ratings,N,r0):
    df_rating_info = df_ratings.groupby(['movieId']).agg(count_rate=('userId','count'),median_rate=('rating','median'),mean_rate=('rating','mean'),max_rate=('rating','max'),min_rate=('rating','min'))
    df_rating_info_popularN = df_rating_info.loc[df_rating_info['count_rate']>N]
    df_ratings_movie_rate_merge_popularN = df_ratings.merge(df_rating_info_popularN,on = ['movieId'])
    df_ratings_movie_rate_merge_popularN_high_rate = df_ratings_movie_rate_merge_popularN[df_ratings_movie_rate_merge_popularN['rating']>r0]

    df_ratings_long_popN_high_rate = df_ratings_movie_rate_merge_popularN_high_rate.pivot(index='userId',columns='movieId',values='rating')
    df_ratings_long_popN_high_rate = df_ratings_long_popN_high_rate.dropna(axis = 0, thresh = 1)
    films_id_popN_high_rate = list(df_ratings_long_popN_high_rate.columns)
    users_id_popN_high_rate= list(df_ratings_long_popN_high_rate.index)

    df_ratings_long_mean_film_popN_high_rate = df_ratings_long_popN_high_rate.fillna(df_ratings_long_popN_high_rate.mean())

    return df_ratings_long_mean_film_popN_high_rate,films_id_popN_high_rate,users_id_popN_high_rate


def find_very_popular_movies(df_ratings,df_movies):
    df_rating_info = df_ratings.groupby(['movieId']).agg(count_rate=('userId','count'))
    df_temp1 = df_rating_info.loc[df_rating_info['count_rate']>200]
    df_temp2 = df_ratings.merge(df_temp1,on = ['movieId'])
    df_very_popular = df_temp2[df_temp2['rating']>3]

    df_very_popular_movies= pd.merge(df_movies,df_very_popular, on = ['movieId'])
    very_pop_movies_name_list = list(df_very_popular_movies['title'].unique())
    # print(len(very_pop_movies_name_list))
    return very_pop_movies_name_list