import streamlit as st
import pandas as pd
import numpy as np
import time

# Set page config
st.set_page_config(page_title="🎬 Movie Recommender", page_icon="🎞️", layout="wide")

# Sidebar
st.sidebar.title("About Project")
st.sidebar.write("This is a simple **Movie Recommendation System** built using:")
st.sidebar.markdown("""
- Python 🐍  
- Pandas 📊  
- Scikit-Learn 🤖  
- Streamlit 🌐  
- Dataset: MovieLens 🎥
""")
st.sidebar.write("✨ Built with ❤️ by Prathuuuu")

# Load data
movies = pd.read_csv('movies.csv')
ratings = pd.read_csv('ratings.csv')

# Merge both datasets
data = pd.merge(ratings, movies, on='movieId')

# Create pivot table: user-movie rating matrix
movie_user_matrix = data.pivot_table(index='userId', columns='title', values='rating')

# Recommendation function
def get_recommendations(movie_name, min_ratings=50):
    target_movie_ratings = movie_user_matrix[movie_name]
    similar_movies = movie_user_matrix.corrwith(target_movie_ratings)
    corr_df = pd.DataFrame(similar_movies, columns=['Correlation'])
    corr_df.dropna(inplace=True)
    rating_count = data.groupby('title')['rating'].count()
    corr_df = corr_df.join(rating_count)
    recommendations = corr_df[corr_df['rating'] > min_ratings].sort_values('Correlation', ascending=False)
    return recommendations.head(10)

# Main App
st.title("🎬 Movie Recommendation System")

st.write("##### Select a movie and get the top 10 recommendations instantly!")

movie_list = movie_user_matrix.columns.tolist()
selected_movie = st.selectbox("Choose a movie:", movie_list)

if st.button("Recommend ❤️"):
    with st.spinner("Finding best recommendations... please wait 💫"):
        time.sleep(1)  # Just to show spinner effect
        try:
            recommendations = get_recommendations(selected_movie)
            st.success("Here are your recommendations 🎯")
            st.dataframe(recommendations)
        except:
            st.warning("Sorry, not enough data for this movie!")

# Footer
st.write("---")
st.write("✅ **Project Complete | Keep Learning & Building 🚀**")
