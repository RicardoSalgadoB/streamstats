from fastapi import FastAPI, status

# Import everything, its a weird approach I'll grant that
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
    find_episodes,
    find_genre,
    rate_movie,
    rate_series,
    rate_episode,
    add_movie,
    add_series,
    add_episode,
    add_genre,
    remove_movie,
    remove_series,
    remove_episode,
    remove_genre,
    update_movie,
    update_series,
    update_episode,
    update_genre,
)

# Declare App
app = FastAPI()

# Movie methods 
app.get("/movies", name="show_movies")(show_movies)
app.get("/movies/find", name="find_movie")(find_movie)

# Series methods
app.get("/series", name="show_series")(show_series)
app.get("/series/find", name="find_series")(find_series)
app.get("/series/episodes", name="find_episodes")(show_eps_of_series)
app.get("/episodes/find", name="find_episodes")(find_episodes)

# All content methods
app.get("/content", name="show_content")(show_all)
app.get("/content/find", name="find_content")(find_content)

# Genre methods
app.get("/genres", name="show_genres")(show_genres)
app.get("/genres/{name}", name="find_genre")(find_genre)
app.get("/genres/{name}/movies", name="show_movies_by_genre")\
    (show_movies_by_genre)
app.get("/genres/{name}/series", name="show_series_by_genre")\
    (show_series_by_genre)
app.get("/genres/{name}/content", name="show_content_by_genre")\
    (show_content_by_genre)
    
# Rating methods
app.post("/movies/{name}/rate", name="rate a movie")(rate_movie)
app.post("/series/{name}/rate", name="rate a series")(rate_series)
app.post("/series/{series_name}/episodes/{name}/rate", name="rate an episode")\
    (rate_episode)

# Adding content methods
app.post("/movies", name="add a movie", status_code=status.HTTP_201_CREATED)\
    (add_movie)
app.post("/series", name="add a series", status_code=status.HTTP_201_CREATED)\
    (add_series)
app.post("/series/{series_name}/episodes", name="add an episode", status_code=status.HTTP_201_CREATED)\
    (add_episode)
app.post("/genres", name="add a genre", status_code=status.HTTP_201_CREATED)\
    (add_genre)

# Delete content methods
app.delete("/movies/{name}", name="remove a movie")(remove_movie)
app.delete("/series/{name}", name="remove a series")(remove_series)
app.delete("/series/{series_name}/episodes/{name}", name="remove an episode")\
    (remove_episode)
app.delete("/genres/{name}", name="remove a genre")(remove_genre)

# Update content
app.patch("/movies/{name}", name="update a movie")(update_movie)
app.patch("/series/{name}", name="update a series")(update_series)
app.patch("/series/{series_name}/episodes/{name}", name="update an episode")\
    (update_episode)
app.patch("/genres/{name}", name="update a genre")(update_genre)