import random
import numpy as np
import pandas as pd
# from recommend_some_movies import recommend_random
from dataframes import read_movie_data
from dataframes import find_very_popular_movies
from dataframes import filter_popular_high_rate

from sklearn.decomposition import NMF
from sklearn.metrics.pairwise import cosine_similarity

import warnings
warnings.filterwarnings("ignore")


df_movies,df_ratings = read_movie_data()
df_ratings_long = df_ratings.pivot(index='userId',columns='movieId',values='rating')
all_movies = list(df_ratings_long.columns)

very_pop_movies_name_list = find_very_popular_movies(df_ratings,df_movies) 
# print(very_pop_movies_name_list)

class MovieRecommendation:
    def __init__(self, user_input, k=5):
        self.user_input = user_input
        self.k = int(user_input["numrec"])
    
    def recommend_movie(self):
        if self.user_input["method"] == "random":
            random.shuffle(all_movies)
            return all_movies[:self.k]
        # --------------------------------------------------
        else:

            best_feature_num = 42 
            best_min_rate_number = 150
            best_min_rate = 2

            features_list = []
            for i in range(best_feature_num):
                features_list.append(f'feature{i}')
            

            pop_id_int = [356, 318, 296, 593, 2571, 480, 110, 589, 527, 2959, 1, 1196, 2858, 50, 47, 780, 150]
            pop_dict = {}
            for i in pop_id_int:
                pop_dict[i] = self.user_input[str(i)]


            seen_movies = []
            for key, value in pop_dict.items():
                if value:
                    seen_movies.append(key)
                else:
                    pop_dict[key]=0

            target_user = 99999 #'new_user'
            pop_df = pd.DataFrame(pop_dict,columns = pop_id_int, index = [target_user])
            pop_df = pop_df.fillna(0)


            df, f_id, u_id= filter_popular_high_rate(df_ratings,best_min_rate_number,best_min_rate)
            # # df.to_csv('ml-latest-small/top_movies.csv')

            # df = pd.read_csv('ml-latest-small/top_movies.csv', index_col='userId')
            # f_id = list(df.columns)
            # u_id = list(df.index)
            # df.rename(columns=lambda x: int(x), inplace=True)

            df_new_user = pd.concat([df,pop_df], axis=0)
            df_new_user = df_new_user.fillna(0)

            u_id = u_id + [target_user]
            user_unseen_movies = [i for i in f_id if i not in seen_movies]

            
            # print('*****************')
            # # print({column: type(column) for column in pop_df.columns})
            # print(df.shape)
            # print(pop_df.shape)
            # print(df_new_user.shape)

            # print('*****************')

            if self.user_input["method"] == "nmf":
                nmf = NMF(n_components = best_feature_num, init = 'nndsvda', max_iter = 300)
                nmf.fit(df_new_user)
                Q = pd.DataFrame(nmf.components_, 
                                columns = f_id, 
                                index = features_list)
                P = pd.DataFrame(nmf.transform(df_new_user), 
                                columns = features_list, 
                                index = u_id)
                recommendations_reconstructed = pd.DataFrame(np.dot(P, Q), 
                                                index = u_id, 
                                                columns = f_id)
                # all_non_filtered_movies = list(recommendations_reconstructed.columns)


                user_calculated_rate = pd.DataFrame()
                # movieID_list = []
                for ii in user_unseen_movies:    

                    rate=recommendations_reconstructed.loc[target_user,ii]
                    line_df = pd.DataFrame({'movieId':[ii], 'rate':[rate]})
                    user_calculated_rate = pd.concat([user_calculated_rate,line_df], axis=0)
                    # user_calculated_rate = user_calculated_rate.append({'movieId':ii, 'rate':rate},ignore_index=True)
                    
                sorted = user_calculated_rate.sort_values(by = ['rate'], ascending=False)
                sorted_head = sorted.head(self.k)
                # sorted_head['movieId'] = sorted_head['movieId'].astype(int)

                
                NMF_sorted_head_merge = pd.merge(df_movies,sorted_head, on = ['movieId'])
                result_NMF_max = NMF_sorted_head_merge.sort_values("rate", ascending = False)
                # --------------    
                return result_NMF_max['title']
                # return user_unseen_movies
            
            # /////////////////////////////////////////////////////
            # /////////////////////////////////////////////////////
            # /////////////////////////////////////////////////////
            # /////////////////////////////////////////////////////

            if self.user_input["method"] == "cosine":
                # df, u, f = filter_popular_high_rate(df_ratings,best_min_rate_number,best_min_rate)
                # print(cosine_similarity(df_new_user).shape)
                # print(len(u_id))
                # print(len(f_id))
                cosine_tab = pd.DataFrame(cosine_similarity(df_new_user), 
                                                index = u_id, 
                                                columns = u_id)
                # print(cosine_tab[target_user])
                neighbors = list(cosine_tab[target_user].sort_values(ascending = False).index[1:10])
                # neighbors = list(cosine_tab[target_user])#.index[1:10])

                # print(neighbors)

            predicted_ratings_movies = []
            rating_T = df_new_user.T          

            # for movie in unseen_movies:
            for movie in user_unseen_movies:
                # list people who watched the unseen movies
                others = list(rating_T.columns[rating_T.loc[movie] > 0])
                numerator = 0
                denominator = 0.000001
                # go through users who are similar but watched the film
                for user in neighbors:
                    if user in others:

                        rating = rating_T.loc[movie, user]
                        similarity = cosine_tab.loc[target_user, user]
                        # print(similarity)
                        numerator = numerator + rating * similarity
                        denominator = denominator + similarity

                predicted_ratings = round(numerator / denominator, 1)
                predicted_ratings_movies.append([predicted_ratings, movie])

            predicted_rating_df = pd.DataFrame(predicted_ratings_movies, columns = ["rating", "movieId"])
            sorted_cosine = predicted_rating_df.sort_values("rating", ascending = False)
            sorted_cosine_head = sorted_cosine.head(self.k)
            cosine_sorted_head_merge = pd.merge(df_movies,sorted_cosine_head, on = ['movieId'])
            result_cosine_max = cosine_sorted_head_merge.sort_values("rating", ascending = False)
            print(result_cosine_max)
            # print(neighbors)
            print('?????????????/////////////')
            # print(others)
            return result_cosine_max['title']

if __name__ == "__main__":
    print('********')
    user_input = {"method": "nmf", "movie_1":3, "movie_2": 4}
    print('????????')
    inst = MovieRecommendation(user_input=user_input,k = 6)
    print('////////')
    recs = inst.recommend_movie()
    print(recs)



