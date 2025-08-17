document.addEventListener("DOMContentLoaded", function () { 
    const chatBox = document.getElementById("chat-box");
    const userInput = document.getElementById("user-input");
    const sendButton = document.getElementById("send-btn");
    const movieSearchInput = document.getElementById("movie-search");
    const movieSearchButton = document.getElementById("search-movie-btn");
    const movieResultContainer = document.getElementById("movie-result");

    function addMessage(sender, message) {
        chatBox.innerHTML += `<div><b>${sender}:</b> ${message}</div>`;
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    function displayMovieDetails(movie) {
        if (!movie || movie.Response === "False") {
            movieResultContainer.innerHTML = `<p style="color: red;">❌ Movie not found or API limit reached.</p>`;
        } else {
            movieResultContainer.innerHTML = `
                <div style="margin: 10px 0; padding: 15px; background: #222; color: #fff; border-radius: 8px; display: flex; flex-wrap: wrap;">
                    <img src="${movie.Poster !== "N/A" ? movie.Poster : 'placeholder.jpg'}" 
                         alt="${movie.Title} Poster" 
                         width="150" 
                         style="border-radius: 8px; margin-right: 15px;">
                    <div>
                        <h2>🎥 ${movie.Title} (${movie.Year})</h2>
                        <p><strong>📖 Plot:</strong> ${movie.Plot || "Not available"}</p>
                        <p><strong>🎭 Genre:</strong> ${movie.Genre || "Not available"}</p>
                        <p><strong>🎬 Director:</strong> ${movie.Director || "Not available"}</p>
                        <p><strong>🎭 Actors:</strong> ${movie.Actors || "Not available"}</p>
                        <p><strong>⭐ IMDb Rating:</strong> ${movie.imdbRating || "Not available"}</p>
                    </div>
                </div>
            `;
        }
    }

    function searchMovie() {
        let movieQuery = movieSearchInput.value.trim();
        if (movieQuery === "") return;

        movieResultContainer.innerHTML = `<p style="color: yellow;">🔍 Searching for <b>${movieQuery}</b>...</p>`;

        fetch("/search_movie", {
            method: "POST",
            body: new URLSearchParams({ movie_name: movieQuery }),
            headers: { "Content-Type": "application/x-www-form-urlencoded" }
        })
        .then(response => response.json())
        .then(movie => displayMovieDetails(movie))
        .catch(error => console.error("Movie Search Error:", error));

        movieSearchInput.value = "";
    }

    movieSearchButton.addEventListener("click", searchMovie);
});
