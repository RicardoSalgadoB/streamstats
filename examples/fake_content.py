import os
import random
from typing import List
import json

from dotenv import load_dotenv
import sqlalchemy as sa
import sqlalchemy.orm as orm

from app.models import Movie, Episode, Series, Genre

from examples.fake_generator import generate_fake_title

load_dotenv()
db_url = os.getenv("DB_URL")
ENGINE = sa.create_engine(db_url)


def generate_genres() -> List[Genre]:
    # Got names from Wikipedis, swapped one
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
    
    for name in genre_names:
        genre_objs.append(Genre(name=name))
        
    return genre_objs


def generate_movies() -> List[Movie]:
    movies = []
    names =[]
    for _ in range(5000):
        n = generate_fake_title()
        names.append(n)
        movies.append(Movie(
            name=n, 
            duration=random.randint(100, 240)
        ))
        with open('names/movie_names.txt', 'w') as f:
            for n in names:
                f.write(n + '\n')
    return movies


def generate_series():
    series = []
    series_names: dict[str, List[str]] = {}
    for _ in range(2000):
        name = generate_fake_title()
        series.append(Series(name=name))
        series_names[name] = []
    return series, series_names
        
        
def generate_episodes(series: List[Series], series_names: dict[str, List[str]]) -> None:
    for _ in range(20000):
        ep_name = generate_fake_title()
        s = random.choice(series)
        s.episodes.append(Episode(
            name=ep_name,
            duration=random.randint(5, 100),
            season=random.randint(1, 10)
        ))
        series_names[s.name].append(ep_name)
        
    with open("series.json", "w") as f:
        json.dump(series_names, f)
        
        
def embed_genres(
    genres: List[Genre], 
    movies: List[Movie], 
    series: List[Series]
) -> None:
    for m in movies:
        gnr_set = {random.choice(genres) for _ in range(random.randint(1, 5))}
        for gnr in list(gnr_set):
            m.genres.append(gnr)
        
    for s in series:
        gnr_set = {random.choice(genres) for _ in range(random.randint(1, 5))}
        for gnr in list(gnr_set):
            s.genres.append(gnr)
            for ep in s.episodes:
                ep.genres.append(gnr)
                
                
if __name__ == '__main__':
    genres = generate_genres()
    movies = generate_movies()
    series, series_names = generate_series()
    generate_episodes(series, series_names)
    embed_genres(genres, movies, series)
    
    with orm.Session(ENGINE) as session:
        for g in genres:
            session.add(g)
        for m in movies:
            session.add(m)
        for s in series:
            session.add(s)
        session.commit()