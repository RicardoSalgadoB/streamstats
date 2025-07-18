from app.utils import (
    show_movies,
    show_series,
    show_all,
    show_genres,
    show_movies_by_genre,
    show_series_by_genre,
    show_content_by_genre,
    show_eps_of_series,
    find_movie,
    find_series,
    find_episode,
    rate_movie,
    rate_series,
    rate_episode,
    Rating
)
from fastapi import FastAPI

app = FastAPI()

@app.get("/", name="index")
def index():
    return {
        "/movies",
        "/series",
        "/content",
        "/genres"
    }
    
app.get("/movies", name="show_movies")(show_movies)
app.get("/series", name="show_series")(show_series)
app.get("/content", name="show_content")(show_all)
app.get("/genres", name="genres")(show_genres)
app.get("/movies/genre", name="show_movies_by_genre")\
    (show_movies_by_genre)
app.get("/series/genre", name="show_series_by_genre")\
    (show_series_by_genre)
app.get("/content/genre", name="show_content_by_genre")\
    (show_content_by_genre)
app.get("/series/{name}/episodes", name="show_episodes_of_series")\
    (show_eps_of_series)
app.get("/movies/{name}", name="find_movie")(find_movie)
app.get("/series/{name}", name="find_series")(find_series)
app.get("/series/{series_name}/episodes/{name}", name="find_episodes")\
    (find_episode)
    
app.post("/rate/movie", name="rate a movie")(rate_movie)
app.post("/rate/series", name="rate a series")(rate_series)
app.post("/rate/episode", name="rate an episode")(rate_episode)