import os
import random

from dotenv import load_dotenv
import sqlalchemy as sa
import sqlalchemy.orm as orm

from app.models import Movie, Episode, Series, Genre
from typing import List

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
    for _ in range(5000):
        movies.append(Movie(
            name=generate_fake_title(), 
            duration=random.randint(100, 240)
        ))
    return movies


def generate_series() -> List[Series]:
    series = []
    for _ in range(2000):
        series.append(Series(name=generate_fake_title()))
    return series
        
        
def generate_episodes(series: List[Series]) -> None:
    for _ in range(20000):
        random.choice(series).episodes.append(Episode(
            name=generate_fake_title(),
            duration=random.randint(5, 100),
            season=random.randint(1, 10)
        ))
        
        
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
    series = generate_series()
    generate_episodes(series)
    embed_genres(genres, movies, series)
    
    with orm.Session(ENGINE) as session:
        for g in genres:
            session.add(g)
        for m in movies:
            session.add(m)
        for s in series:
            session.add(s)
        session.commit()