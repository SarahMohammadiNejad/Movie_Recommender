# Movie-recommender
This application recommends movies to you based on the scores you give to the first top 17 movies! You can run it on
https://sarah-movierecommender.onrender.com

if in any case this deployed version won't work, you can run it localy using:

python application.py

### What this application does
We create a flask application that ask the user to enter her/his scores for the 20 most famous movies (can also scoring to the unseen movies). It also needs some information from user. 
1- The number of movies user wants as recommendation.  
2- The method to find the movies which so far random, NMF, and cosine similarity are implemented. 
This application use MovieLens dataset:
https://grouplens.org/datasets/movielens/
in which over, 610 users gave score to 193609 movies and from this dataset we find 
- the most relevant features and Q and P matrix for NMF method
- most similar neighbors to targer user
