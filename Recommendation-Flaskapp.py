from flask import Flask, render_template, request, url_for, flash, redirect
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def create_matrix():
    movie_df=pd.read_csv('C:/Users/mohit/movies_features_combined.csv')
    cv = CountVectorizer(stop_words='english')
    count_matrix = cv.fit_transform(movie_df['combined'])
    sim = cosine_similarity(count_matrix, count_matrix)
    return movie_df, sim

def recommend_movie(m):
    m=m.lower()
    try:
        movie_df.head()
        sim.shape

    except:
        movie_df, sim=create_matrix()

    if m not in movie_df['title'].unique():
        return("This movies is not in our database, Please check if you spelled it correct")
    else:
        indices = pd.Series(movie_df.index,index=movie_df['title']).drop_duplicates()
        idx = indices[m]
        sim_scores = list(enumerate(sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x:x[1], reverse=True)
        sim_scores = sim_scores[1:11]
        l = []
        for i in range(len(sim_scores)):
            a = sim_scores[i][0]
            l.append(movie_df['title'][a])
        return l

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/content_based")
def Content_Recommend():
    return render_template('Content_Recommendation.html')

@app.route("/recommendation")
def recommend():
    movie = request.args.get('movie')
    r = recommend_movie(movie)
    movie = movie.upper()
    if type(r) == type('string'):
        return render_template('recommendations.html', movie=movie, r=r, t='s')
    else:
        return render_template('recommendations.html', movie=movie, r=r, t='l')

if __name__ == '__main__':
    app.debug = True
    app.run()