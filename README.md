🍿 Movie Chatbot
🍿 Movie Chatbot is an intelligent Python-Flask application that serves as your personal cinematic assistant. It uses a trained machine learning model to understand your queries and fetch movie details and genre-based recommendations from the OMDb API. Discover your next favorite film in a chat-based experience!

✨ Features
🎬 Movie Search: Find detailed information (plot, year, cast, etc.) for a specific movie title.

🎭 Genre Recommendations: Get a list of top movies based on popular genres (e.g., action, comedy, thriller).

🤖 Intelligent Chat: Uses a machine learning model to understand user intents and provide relevant responses.

🎵 Audio Feedback: Provides audio cues for certain responses (e.g., movie not found).

🚀 Getting Started
Prerequisites
Before you begin, make sure you have the following installed:

Python 3.x

pip (Python package installer)

Installation

Install the required libraries:

pip install -r requirements.txt

Note: You'll need to create a requirements.txt file based on the libraries in your code, such as Flask, pandas, scikit-learn, and requests. You can generate this automatically with pip freeze > requirements.txt.

Get your OMDb API Key:

Visit the OMDb API website.

Sign up for a free API key and replace "a6ceb0e5" in your app.py file with your new key.

Prepare the dataset:

The project relies on a pre-trained model and movie datasets. You mentioned local paths in your code, so you'll need to create a similar directory structure and place your files there.

Create a model directory and place trained_model.pkl inside it.

Create an archive directory within a aipro1 folder at the root of your project, and place your genre-specific .csv files inside.

Create an intents.csv file for the model training. This file should have two columns: text and intent.

Create an audio folder and place movie_not_found.mp3 there.

Running the App
Start the Flask server:

python app.py

Open your browser and go to http://127.0.0.1:5000 to start chatting with the bot!

📂 Project Structure
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── templates/
│   └── index.html      # Frontend for the chatbot interface
├── static/
│   ├── css/
│   └── js/
├── audio/
│   └── movie_not_found.mp3 # Audio files for responses
├── model/
│   └── trained_model.pkl   # Pre-trained chatbot model
└── aipro1/
    └── archive/
        ├── action.csv      # Example genre CSV
        └── comedy.csv      # Example genre CSV

🛠️ Built With
Flask - The web framework used

Scikit-learn - For the machine learning model

Pandas - For data handling

Requests - For making API calls to OMDb

OMDb API - The movie database used

🤝 Contributing
Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are greatly appreciated.

Fork the Project

Create your Feature Branch (git checkout -b feature/AmazingFeature)

Commit your Changes (git commit -m 'Add some AmazingFeature')

Push to the Branch (git push origin feature/AmazingFeature)

Open a Pull Request



📧 Contact
Your Name - Aravindbtc2005@gmail.com.com

Project Link:  https://github.com/aravindbtc/-Movie-Chatbot.git

