# Movie-recommender
This application is meant to recommend movies to users on a browser:
https://sarah-movierecommender.onrender.com

it can also been run using python application.py


We create a flask application that ask the user to enter her/his scores for the 20 most famous movies (can also scoring to the unseen movies). It also needs some information from user. 
1- The number of movies user wants as recommendation.  
2- The method to find the movies which so far random, NMF, and cosine similarity are implemented. 
This application use MovieLens dataset:
https://grouplens.org/datasets/movielens/
in which over, 610 users gave score to 193609 movies and from this dataset we find 
- the most relevant features and Q and P matrix for NMF method
- most similar neighbors to targer user
