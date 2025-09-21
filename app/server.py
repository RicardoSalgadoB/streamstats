from fastapi import FastAPI, status

# Import everything, its a weird approach I'll grant thata, but hey no bloat in this file
from app.utils import (
    # Show
    show_movies,
    show_series,
    show_all,
    show_genres,
    
    # Show by Genre/Series
    show_movies_by_genre,
    show_series_by_genre,
    show_content_by_genre,
    show_eps_of_series,
    
    # Find
    find_content,
    find_movie,
    find_series,
    find_episodes,
    find_genre,
    
    # Rate
    rate_content,
    rate_movie,
    rate_series,
    rate_episode,
    
    # Add content
    add_movie,
    add_series,
    add_episode,
    add_genre,
    
    # Remove content
    remove_movie,
    remove_series,
    remove_episode,
    remove_genre,
    
    # Update content
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
app.get("/genres/find", name="find_genre")(find_genre)
app.get("/genres/movies", name="show_movies_by_genre")(show_movies_by_genre)
app.get("/genres/series", name="show_series_by_genre")(show_series_by_genre)
app.get("/genres/content", name="show_content_by_genre")(show_content_by_genre)
    
# Rating methods
app.post("/content/rate", name="rate a movie")(rate_content)
app.post("/movies/rate", name="rate a movie")(rate_movie)
app.post("/series/rate", name="rate a series")(rate_series)
app.post("/series/episodes/rate", name="rate an episode")(rate_episode)

# Adding content methods
app.post("/movies", name="add a movie", status_code=status.HTTP_201_CREATED)\
    (add_movie)
app.post("/series", name="add a series", status_code=status.HTTP_201_CREATED)\
    (add_series)
app.post("/episodes", name="add an episode", status_code=status.HTTP_201_CREATED)\
    (add_episode)
app.post("/genres", name="add a genre", status_code=status.HTTP_201_CREATED)\
    (add_genre)

# Delete content methods
app.delete("/movies/remove", name="remove a movie")(remove_movie)
app.delete("/series/remove", name="remove a series")(remove_series)
app.delete("/episodes/remove", name="remove an episode")(remove_episode)
app.delete("/genres/remove", name="remove a genre")(remove_genre)

# Update content
app.patch("/movies/update", name="update a movie")(update_movie)
app.patch("/series/update", name="update a series")(update_series)
app.patch("/episodes/update", name="update an episode")(update_episode)
app.patch("/genres/update", name="update a genre")(update_genre)