import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=b19836dfa6c80e686a0b92105311f20a&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_poster = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch poster from API
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_poster

# Load movie data and similarity data
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movies Recommender System')

selected_movie_name = st.selectbox('Wish your movie?', movies['title'].values)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    # Create a layout with columns for each movie
    cols = st.columns(5)  # Create 5 columns for 5 movies

    for i in range(len(names)):
        with cols[i % 5]:  # Use modulo to wrap around columns
            st.image(posters[i], caption=names[i], use_container_width='auto')  # Display the poster
            # st.text(names[i])  # Display the movie name

# import streamlit as st
# import pickle
# import pandas as pd
# import requests
#
# def  fetch_poster(movie_id):
#     response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=b19836dfa6c80e686a0b92105311f20a&language=en-US'.format(movie_id))
#     data = response.json()
#
#     return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
#
# def recommend(movie):
#     movie_index = movies[movies['title'] == movie].index[0]
#     distances = similarity[movie_index]
#     movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
#
#     recommended_movies = []
#     recommended_movies_poster = []
#     for i in movies_list:
#         movie_id = movies.iloc[i[0]].movie_id
#
#         recommended_movies.append(movies.iloc[i[0]].title)
#         # fetch poster from API
#         recommended_movies_poster.append(fetch_poster(movie_id))
#     return recommended_movies,recommended_movies_poster
#
# movies_dict = pickle.load(open('movie_dict.pkl','rb'))
# movies = pd.DataFrame(movies_dict)
#
# similarity = pickle.load(open('similarity.pkl','rb'))
#
# st.title('Movies Recommender System')
#
# selected_movie_name = st.selectbox(
# 'Wish your movie?',movies['title'].values)
#
# if st.button('Recommend'):
#     names,posters = recommend(selected_movie_name)
#     columns = st.columns(5)
#
#     for i in range(5):  # Assuming you want to display exactly 5 movies
#         with columns[i]:
#             st.text(names[i])  # Display the movie name
#             st.image(posters[i], use_container_width=True)
