import streamlit as st
import pickle
import pandas as pd
import requests
import os
import subprocess

# --- Function to download file from Google Drive using gdown ---
def download_from_drive(file_id, dest_path):
    if not os.path.exists(dest_path):
        print(f"Downloading {dest_path} from Google Drive via gdown...")
        subprocess.run(['pip', 'install', 'gdown'])
        subprocess.run(['gdown', f'https://drive.google.com/uc?id={file_id}', '-O', dest_path])
        print(f"✅ {dest_path} download complete!")
    else:
        print(f"{dest_path} already exists, skipping download.")

# --- Download your big file ---
download_from_drive("1r4NYFLY8kozJCU_p6RB12xQf1g31ByeA", "similarity.pkl")

# (optional) movie_dict.pkl ka link bhej do agar wo bhi large hai
# download_from_drive("<MOVIE_DICT_ID>", "movie_dict.pkl")

# --- Load pickles ---
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# --- Poster fetching ---
def fetch_poster(movie_id):
    response = requests.get(
        f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=777baea8a54fd6e6cab675d9cf1621ad&language=en-US'
    )
    data = response.json()
    poster_path = data.get('poster_path')
    if poster_path:
        return "https://image.tmdb.org/t/p/w500/" + poster_path
    else:
        return "https://via.placeholder.com/500x750?text=No+Image+Available"

# --- Recommendation function ---
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

# --- Streamlit UI ---
st.title('🎬 Movie Recommender System')

selected_movie_name = st.selectbox(
    'Select a movie you like:',
    movies['title'].values
)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])