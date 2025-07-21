# Function to populate the catalog with fake content

import os
import random
from typing import List
import json

from dotenv import load_dotenv
import sqlalchemy as sa
import sqlalchemy.orm as orm

from app.models import Movie, Episode, Series, Genre

from examples.fake_generator import generate_fake_title

# Load secret variables
load_dotenv()
db_url = os.getenv("DB_URL")

# Create an sql alchemy engine
ENGINE = sa.create_engine(db_url)


def generate_genres() -> List[Genre]:
    """Generate the genres of the catalog."""
    # Got names from Wikipedia, swapped one (guess which)
    genre_names = [
        "Action",
        "Adventure",
        "Animation",
        "Comedy",
        "Drama",
        "Fantasy",
        "Historical",
        "Horror",
        "Melodrama",
        "Musical",
        "Noir",
        "Romance",
        "Science Fiction",
        "Spies",
        "Thriller",
        "Western"
    ]
    genre_objs = []
    
    # Create each object
    for name in genre_names:
        genre_objs.append(Genre(name=name))
        
    return genre_objs


def generate_movies(num: int = 5000) -> List[Movie]:
    """Generates num fake movies of the catalog."""
    movies = []
    names =[]
    
    for _ in range(num):
        n = generate_fake_title()   # get name
        names.append(n) # add it the names list
            # add the movie object to the list
        movies.append(Movie(
            name=n, 
            duration=random.randint(100, 240)
        ))
            # store the names of the movies in a file for finds during testing
        with open('names/movie_names.txt', 'w') as f:
            for n in names:
                f.write(n + '\n')
    return movies   # return the list of objects


def generate_series(num: int = 2000):
    """Generates num fake series for the catalog."""
    series = []
    series_names: dict[str, List[str]] = {} # dictionary to save series and episodes names
    
    for _ in range(num):
        name = generate_fake_title()
        series.append(Series(name=name))
        series_names[name] = [] # add name to the dict
    return series, series_names # return list and dict
        
        
def generate_episodes(series: List[Series], series_names: dict[str, List[str]], num: int = 20000) -> None:
    """Generate num fake episodes for the catalog."""
    for _ in range(20000):
        ep_name = generate_fake_title()
        s = random.choice(series)   # pick a random series
            # append an episode to it
        s.episodes.append(Episode(
            name=ep_name,
            duration=random.randint(5, 100),
            season=random.randint(1, 10)
        ))
        series_names[s.name].append(ep_name)    # Add the episode to the list of its respective entry
    
    # Once the series-episodes dictinary is comlete, store it on a json file for testing purposes.
    with open("names/series.json", "w") as f:
        json.dump(series_names, f)
        
        
def embed_genres(
    genres: List[Genre], 
    movies: List[Movie], 
    series: List[Series]
) -> None:
    """Add genres to the contents of the catalog."""
    for m in movies:
            # Use set to add the same genre twice to the same movie
        gnr_set = {random.choice(genres) for _ in range(random.randint(1, 5))}
        for gnr in list(gnr_set):
            m.genres.append(gnr)
        
    for s in series:
            # Use set to add the same genre twice to the same series and eps
        gnr_set = {random.choice(genres) for _ in range(random.randint(1, 5))}
        for gnr in list(gnr_set):
            s.genres.append(gnr)
            # Add the genres to each episode
            for ep in s.episodes:
                ep.genres.append(gnr)
                
                
if __name__ == '__main__':
    genres = generate_genres()
    movies = generate_movies()
    series, series_names = generate_series()
    generate_episodes(series, series_names)
    embed_genres(genres, movies, series)
    
    # Commit the objects to the database
    with orm.Session(ENGINE) as session:
        for g in genres:
            session.add(g)
        for m in movies:
            session.add(m)
        for s in series:
            session.add(s)
        session.commit()