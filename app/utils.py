import os
from typing import List, Union
from pydantic import BaseModel
from dotenv import load_dotenv

import sqlalchemy as sa
import sqlalchemy.orm as orm

from app.tables import Content, Movie, Episode, Serie, Genre

load_dotenv()
db_url = os.getenv("DB_URL")
ENGINE = sa.create_engine(db_url)


class Rating(BaseModel):
    name: str
    rating: int

def show_movies() -> List[str]:
    stmt = sa.select(Movie)
    
    with orm.Session(ENGINE) as session:
        movies = session.scalars(stmt)
        return [repr(m) for m in movies]
            
def show_series() -> List[str]:
    stmt = sa.select(Serie)
    
    with orm.Session(ENGINE) as session:
        series = session.scalars(stmt)
        return [repr(s) for s in series]
            
def show_all() -> List[str]:
    return show_movies() + show_series()
    
def show_genres() -> List[str]:
    stmt = sa.select(Genre)
    
    with orm.Session(ENGINE) as session:
        genres = session.scalars(stmt)
        return [repr(g) for g in genres]

def show_movies_by_genre(name: str) -> List[str]:
    stmt = (
        sa.select(Content)
        .join(Genre.contents)
        .where(sa.and_(Genre.name == name, Content.type == "movie"))
        .order_by(Content.id)
    )
    
    with orm.Session(ENGINE) as session:
        movies = session.scalars(stmt)
        return [repr(m) for m in movies]
            
def show_series_by_genre(name: str) -> List[str]:
    stmt = (
        sa.select(Content)
        .join(Genre.contents)
        .where(sa.and_(Genre.name == name, Content.type == "serie"))
        .order_by(Content.id)
    )
    
    with orm.Session(ENGINE) as session:
        series = session.scalars(stmt)
        return [repr(s) for s in series]
            
def show_content_by_genre(name: str) -> List[str]:
    return show_movies_by_genre(name) + show_series_by_genre(name)
    
def show_eps_of_series(name: str) -> Union[str, List[str]]:
    series_stmt = sa.select(Serie).where(Serie.name == name)

    with orm.Session(ENGINE) as session:
        series = session.scalar(series_stmt)
        if series:
            return [repr(ep) for ep in series.episodes]
        else:
            return f"{name} is not a series"
            
def find_movie(name: str) -> str:
    stmt = sa.select(Movie).where(Movie.name == name)
    
    with orm.Session(ENGINE) as session:
        movie = session.scalar(stmt)
        if movie:
            return repr(movie)
        else:
            return f"{name} not found in movies"
            
def find_series(name: str) -> str:
    stmt = sa.select(Serie).where(Serie.name == name)
    
    with orm.Session(ENGINE) as session:
        series = session.scalar(stmt)
        if series:
            return repr(series)
        else:
            return f"{name} not found in series"
            
def find_episode(name: str, series_name: str) -> str:
    stmt = sa.select(Episode).where(Episode.name == name)
    
    with orm.Session(ENGINE) as session:
        ep = session.scalar(stmt)
        if ep and ep.series.name == series_name:
            return repr(ep)
        else:
            return f'{name} not found in the episodes of series "{series_name}"'
        
def rate_movie(r: Rating) -> str:
    rating = r.rating
    name = r.name
    if rating > 5 or rating < 1:
        return "Rating must be between 1 and 5"
    stmt = sa.select(Movie).where(Movie.name == name)
    
    with orm.Session(ENGINE) as session:
        movie = session.scalar(stmt)
        movie.ratings_total += rating
        movie.ratings_number += 1
        session.commit()
        
    return f"The movie {name} has been given a rating of {rating}"
        
def rate_series(r: Rating) -> str:
    rating = r.rating
    name = r.name
    if rating > 5 or rating < 1:
        return "Rating must be between 1 and 5"
    stmt = sa.select(Serie).where(Serie.name == name)
    
    with orm.Session(ENGINE) as session:
        series = session.scalar(stmt)
        series.ratings_total += rating
        series.ratings_number += 1
        session.commit()
        
    return f"The series {name} has been given a rating of {rating}"
        
def rate_episode(r: Rating) -> str:
    rating = r.rating
    name = r.name
    if rating > 5 or rating < 1:
        return "Rating must be between 1 and 5"
    stmt = sa.select(Episode).where(Episode.name == name)
    
    with orm.Session(ENGINE) as session:
        episode = session.scalar(stmt)
        episode.ratings_total += rating
        episode.ratings_number += 1
        session.commit()
        
    return f"The episode {name} has been given a rating of {rating}"