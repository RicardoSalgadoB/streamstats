from app.utils import (
    show_movies,
    show_series,
    show_all,
    show_genres,
    show_movies_by_genre,
    show_series_by_genre,
    show_content_by_genre,
    show_eps_of_series,
    find_content,
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
    
app.get("/movies", name="show_movies")(show_movies)
app.get("/movies/{name}", name="show_movies")(find_movie)

app.get("/series", name="show_series")(show_series)
app.get("/series/{name}", name="show_series")(find_series)
app.get("/series/{name}/episodes", name="show_episodes_of_series")\
    (show_eps_of_series)
app.get("/series/{series_name}/episodes/{name}", name="find_episodes")\
    (find_episode)

app.get("/content", name="show_content")(show_all)
app.get("/content/{name}", name="show_content")(find_content)

app.get("/genres", name="show_genres")(show_genres)
app.get("/genres/{name}/movies", name="show_movies_by_genre")\
    (show_movies_by_genre)
app.get("/genres/{name}/series", name="show_series_by_genre")\
    (show_series_by_genre)
app.get("/genres/{name}/content", name="show_content_by_genre")\
    (show_content_by_genre)
    
app.post("/movies/{name}/rate", name="rate a movie")(rate_movie)
app.post("/series/{name}/rate", name="rate a movie")(rate_series)
app.post("/series/{series_name}/episodes/{name}/rate", name="rate a movie")\
    (rate_episode)