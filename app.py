import streamlit as st
import pickle
import pandas as pd
import requests

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0] # returns index of that movie
    distance = similarity[movie_index] # calculate similarity score with all other movies
    movies_list = sorted(list(enumerate(distance)), reverse=True, key = lambda x : x[1])[1:6] # Extract those movies with 5 best similarity score

    recommended_movie = []
    recommended_movie_poster= []
    for i in movies_list:
        recommended_movie.append(movies.iloc[i[0]].title)
        recommended_movie_poster.append(fetch_poster(movies.iloc[i[0]].movie_id))
    return  recommended_movie, recommended_movie_poster


api = 'bc9832079260cb1590c37cc1f268f3a1'
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api}&language=en-US"
    response = requests.get(url)
    data = response.json()
    return 'https://image.tmdb.org/t/p/original/' + data['poster_path']



st.title('Movie Recommender System')
selected_movie_name = st.selectbox('Movie available', movies['title'])
if st.button('Recommend'):
    recommended_movie,posters = recommend(selected_movie_name)
    poster_width= 200
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.subheader(recommended_movie[0])
        st.image(posters[0], width=poster_width)
    with col2:
        st.subheader(recommended_movie[1])
        st.image(posters[1], width=poster_width)
    with col3:
        st.subheader(recommended_movie[2])
        st.image(posters[2], width=poster_width)
    with col4:
        st.subheader(recommended_movie[3])
        st.image(posters[3], width=poster_width)
    with col5:
        st.subheader(recommended_movie[4])
        st.image(posters[4], width=poster_width)
