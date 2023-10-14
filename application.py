"""
This is the main file where flask is to be launched
"""

# import our flask module
from flask import Flask, render_template, request
from recommend_some_movies import recommend_nmf
from choice_of_method_to_recommend import MovieRecommendation
from dataframes import read_movie_data
from dataframes import find_very_popular_movies
from dataframes import filter_popular_high_rate


# We need to actually tell flask that this is the file that launches it.
app = Flask(__name__)

df_movies,df_ratings = read_movie_data()
df_ratings_long = df_ratings.pivot(index='userId',columns='movieId',values='rating')
all_movies = list(df_ratings_long.columns)

# very_pop_movies_name_list = find_very_popular_movies(df_ratings,df_movies) 
# print(very_pop_movies_name_list)
# name = [m1,m2,m3,m4,m5,m6,m7,m8,m9,m10,m11,m12,m13,m14,m15,m16,m17,m18]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/recommender")
def recommend_movies():

    user_input = dict(request.args)
    recs = MovieRecommendation(user_input).recommend_movie()

    print(recs)
    return render_template("recommendations.html", movies=recs)
# To test if the server can open, we shall make sure that only when this file is used directly is when we can open a new web server
if __name__ == "__main__":
    app.run(debug=True, port=5001)