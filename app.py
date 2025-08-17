from flask import Flask, request, render_template, session, jsonify, send_from_directory
import os  
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
import requests
import pickle

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secret key for session management

# OMDb API Key
OMDB_API_KEY = "a6ceb0e5"
OMDB_URL = "https://www.omdbapi.com/"

# Load the chatbot model if it exists
model_path = 'model/trained_model.pkl'

if os.path.exists(model_path):
    with open(model_path, 'rb') as file:
        model = pickle.load(file)
else:
    # Load the dataset
    df = pd.read_csv('intents.csv')
    X = df['text']
    y = df['intent']

    # Train the model
    model = make_pipeline(CountVectorizer(), MultinomialNB())
    model.fit(X, y)

    # Save the trained model
    os.makedirs('model', exist_ok=True)
    with open(model_path, 'wb') as file:
        pickle.dump(model, file)

# Function to fetch movie details from OMDb API
def search_movie(query):
    try:
        params = {"t": query, "apikey": OMDB_API_KEY}
        response = requests.get(OMDB_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data.get("Response") == "True":
            return {
                "Title": data.get("Title", "N/A"),
                "Year": data.get("Year", "N/A"),
                "Poster": data.get("Poster", "N/A"),
                "Plot": data.get("Plot", "N/A"),
                "Genre": data.get("Genre", "N/A"),
                "Director": data.get("Director", "N/A"),
                "Actors": data.get("Actors", "N/A"),
                "imdbRating": data.get("imdbRating", "N/A")
            }
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"⚠️ Error fetching movie details: {e}")
        return None

# Function to recommend movies based on genre
def recommend_movies(genre):
    folder_path = "C:/Users/aravi/Downloads/aipro1/archive"
    file_name = f"{genre.lower().strip()}.csv"
    file_path = os.path.join(folder_path, file_name)

    if os.path.exists(file_path):
        try:
            df = pd.read_csv(file_path)
            movies = []
            for _, row in df.head(5).iterrows():
                movie_title = row.get("movie_name")
                if movie_title:
                    details = search_movie(movie_title)
                    if details:
                        movies.append(details)
                    else:
                        movies.append({"Title": movie_title, "Details": "Not found"})
            return movies
        except Exception as e:
            print(f"⚠️ Error reading file: {e}")
            return []
    else:
        return []

@app.route('/')
def home():
    session.clear()
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['message'].strip().lower()

    if user_input:
        intent = model.predict([user_input])[0]

        if "movie" in user_input:
            words = user_input.split()
            for word in words:
                if os.path.exists(f"C:/Users/aravi/Downloads/aipro1/archive/{word}.csv"):
                    movies = recommend_movies(word)
                    if movies:
                        response = f"<h3>Here are some {word.capitalize()} movies:</h3><br>"
                        for movie in movies:
                            response += f"<strong>🎥 {movie['Title']} ({movie.get('Year', 'N/A')})</strong><br>"
                            response += f"<p><strong>📝 Plot:</strong> {movie.get('Plot', 'Not available')}</p>"
                            response += f"<p><strong>🎭 Genre:</strong> {movie.get('Genre', 'Not available')}</p>"
                            response += f"<p><strong>🎬 Director:</strong> {movie.get('Director', 'Not available')}</p>"
                            response += f"<p><strong>⭐ IMDb Rating:</strong> {movie.get('imdbRating', 'Not available')}</p>"
                            response += f"<p><strong>🎭 Cast:</strong> {movie.get('Actors', 'Not available')}</p>"

                            # Show the poster only if it exists and is a valid URL
                            poster_url = movie.get("Poster", "")
                            if poster_url and poster_url != "N/A":
                                response += f'<br><img src="{poster_url}" alt="{movie["Title"]} Poster" width="150"><br>'

                            response += "<hr>"  # Separator for multiple movies

                        return jsonify({"response": response, "audio": "/audio/movie_not_found.mp3"})
                    else:
                        return jsonify({"response": f"Sorry, no {word} movies found.<br><audio autoplay><source src='/audio/movie_not_found.mp3' type='audio/mpeg'></audio>", "audio": "/audio/movie_not_found.mp3"})

            response = "What movie genre are you interested in? (e.g., action, comedy, thriller)"
        
        elif intent == 'movie_search':
            response = "What movie title are you looking for?"
            session['stage'] = 'movie_search'
        
        elif session.get('stage') == 'movie_search':
            movie_details = search_movie(user_input)
            if movie_details:
                response = f"<h3>🎥 {movie_details['Title']} ({movie_details['Year']})</h3><br>"
                response += f"<p><strong>📝 Plot:</strong> {movie_details.get('Plot', 'Not available')}</p>"
                response += f"<p><strong>🎭 Genre:</strong> {movie_details.get('Genre', 'Not available')}</p>"
                response += f"<p><strong>🎬 Director:</strong> {movie_details.get('Director', 'Not available')}</p>"
                response += f"<p><strong>⭐ IMDb Rating:</strong> {movie_details.get('imdbRating', 'Not available')}</p>"
                response += f"<p><strong>🎭 Cast:</strong> {movie_details.get('Actors', 'Not available')}</p>"

                # Show the poster only if it's available
                poster_url = movie_details.get("Poster", "")
                if poster_url and poster_url != "N/A":
                    response += f'<br><img src="{poster_url}" alt="{movie_details["Title"]} Poster" width="150"><br>'

                return jsonify({"response": response})
            else:
                response = "Sorry, I couldn't find that movie.<br><audio autoplay><source src='/audio/movie_not_found.mp3' type='audio/mpeg'></audio>"
                return jsonify({"response": response, "audio": "/audio/movie_not_found.mp3"})
            session.clear()
        
        else:
            response = "Hello! I can assist you with movie recommendations or general chat!<br><audio autoplay><source src='/audio/movie_not_found.mp3' type='audio/mpeg'></audio>"
            return jsonify({"response": response, "audio": "/audio/movie_not_found.mp3"})

    return jsonify({"response": "Please enter a valid message."})

@app.route('/search_movie', methods=['POST'])
def search_movie_route():
    query = request.form.get('movie_name')
    if not query:
        return jsonify({"error": "No movie name provided"}), 400  # ✅ Proper error handling

    movie_details = search_movie(query)

    if movie_details:
        return jsonify(movie_details)
    else:
        return jsonify({"error": "Movie not found"}), 404  # ✅ Proper response when movie is not found

if __name__ == '__main__':
    app.run(debug=True)
