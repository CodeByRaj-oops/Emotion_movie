# app/recommender.py
import os
import requests
from dotenv import load_dotenv

# Load API keys from .env
load_dotenv()
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

if not TMDB_API_KEY:
    raise ValueError("❌ TMDB_API_KEY not found in .env file")

# Emotion → TMDb genre mapping
EMOTION_TO_GENRE = {
    "happy": ["Comedy", "Adventure", "Family"],
    "sad": ["Comedy", "Romance", "Drama"],
    "angry": ["Action", "Thriller", "Crime"],
    "fear": ["Horror", "Thriller"],
    "surprise": ["Mystery", "Fantasy", "Sci-Fi"],
    "disgust": ["Drama", "Mystery"],
    "neutral": ["Drama", "Family"]
}

# TMDb Genre IDs (fixed)
TMDB_GENRES = {
    "Action": 28,
    "Adventure": 12,
    "Animation": 16,
    "Comedy": 35,
    "Crime": 80,
    "Documentary": 99,
    "Drama": 18,
    "Family": 10751,
    "Fantasy": 14,
    "History": 36,
    "Horror": 27,
    "Music": 10402,
    "Mystery": 9648,
    "Romance": 10749,
    "Sci-Fi": 878,
    "TV Movie": 10770,
    "Thriller": 53,
    "War": 10752,
    "Western": 37
}

def get_movies_for_emotion(emotion, num_results=5):
    """
    Fetch movie recommendations from TMDb based on detected emotion.
    Returns list of dicts: [{title, poster_url}, ...]
    """
    emotion = emotion.lower()

    if emotion not in EMOTION_TO_GENRE:
        print(f"⚠️ Unknown emotion '{emotion}', using 'neutral'")
        genres = EMOTION_TO_GENRE["neutral"]
    else:
        genres = EMOTION_TO_GENRE[emotion]

    movies = []
    for genre in genres:
        genre_id = TMDB_GENRES.get(genre)
        if not genre_id:
            continue

        url = (
            f"https://api.themoviedb.org/3/discover/movie"
            f"?api_key={TMDB_API_KEY}&with_genres={genre_id}"
            f"&sort_by=popularity.desc&language=en-US&page=1"
        )
        try:
            response = requests.get(url)
            data = response.json().get("results", [])
            for movie in data[:num_results]:
                poster_url = (
                    f"https://image.tmdb.org/t/p/w500{movie['poster_path']}"
                    if movie.get("poster_path") else None
                )
                movies.append({
                    "title": movie["title"],
                    "poster_url": poster_url
                })
        except Exception as e:
            print(f"Error fetching movies for genre {genre}: {e}")

    return movies


if __name__ == "__main__":
    # Quick test
    test_emotion = "happy"
    recs = get_movies_for_emotion(test_emotion, num_results=3)
    print(f"Recommendations for '{test_emotion}':")
    for m in recs:
        print(f"- {m['title']} ({m['poster_url']})")
