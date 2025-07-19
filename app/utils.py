import os
import json

from typing import List, Union
from pydantic import BaseModel
from dotenv import load_dotenv

import sqlalchemy as sa
import sqlalchemy.orm as orm

from app.models import Content, Movie, Episode, Series, Genre, Rating

load_dotenv()
db_url = os.getenv("DB_URL")
ENGINE = sa.create_engine(db_url)


class RawRating(BaseModel):
    score: int


def show_movies() -> List[dict]:
    stmt = sa.select(Movie)
    
    with orm.Session(ENGINE) as session:
        movies = session.scalars(stmt)
        return [m.to_dict() for m in movies]
    
            
def show_series() -> List[dict]:
    stmt = sa.select(Series)
    
    with orm.Session(ENGINE) as session:
        series = session.scalars(stmt)
        return [s.to_dict() for s in series]
         
            
def show_all() -> List[dict]:
    return show_movies() + show_series()
    
    
def show_genres() -> List[dict]:
    stmt = sa.select(Genre)
    
    with orm.Session(ENGINE) as session:
        genres = session.scalars(stmt)
        return [g.to_dict() for g in genres]


def show_movies_by_genre(name: str) -> List[dict]:
    stmt = (
        sa.select(Content)
        .join(Genre.contents)
        .where(sa.and_(Genre.name == name, Content.type == "movie"))
        .order_by(Content.id)
    )
    
    with orm.Session(ENGINE) as session:
        movies = session.scalars(stmt)
        return [m.to_dict() for m in movies]
          
            
def show_series_by_genre(name: str) -> List[dict]:
    stmt = (
        sa.select(Content)
        .join(Genre.contents)
        .where(sa.and_(Genre.name == name, Content.type == "serie"))
        .order_by(Content.id)
    )
    
    with orm.Session(ENGINE) as session:
        series = session.scalars(stmt)
        return [s.to_dict() for s in series]
            
            
def show_content_by_genre(name: str) -> List[dict]:
    return show_movies_by_genre(name) + show_series_by_genre(name)
    
    
def show_eps_of_series(name: str) -> Union[dict, List[dict]]:
    series_stmt = sa.select(Series).where(Series.name == name)

    with orm.Session(ENGINE) as session:
        series = session.scalar(series_stmt)
        if series:
            return [ep.to_dict() for ep in series.episodes]
        else:
            return {
                "message": f"{name} is not a series"
            }
            

def find_content(name: str) -> dict:
    stmt = sa.select(Content).where(Content.name == name)
    
    with orm.Session(ENGINE) as session:
        content = session.scalar(stmt)
        if content:
            return content.to_dict()
        else:
            return {
                "message": f"{name} not found in Movies"
            }
    

def find_movie(name: str) -> dict:
    stmt = sa.select(Movie).where(Movie.name == name)
    
    with orm.Session(ENGINE) as session:
        movie = session.scalar(stmt)
        if movie:
            return movie.to_dict()
        else:
            return {
                "message": f"{name} not found in movies"
            }
            
            
def find_series(name: str) -> dict:
    stmt = sa.select(Series).where(Series.name == name)
    
    with orm.Session(ENGINE) as session:
        series = session.scalar(stmt)
        if series:
            return series.to_dict()
        else:
            return {
                "message": f"{name} not found in series"
            }
            
            
def find_episode(name: str, series_name: str) -> dict:
    stmt = sa.select(Episode).where(Episode.name == name)
    
    with orm.Session(ENGINE) as session:
        ep = session.scalar(stmt)
        if ep and ep.series.name == series_name:
            return ep.to_dict()
        else:
            return {
                "messages": f"{name} not found in the episodes of the series: '{series_name}'"
            }
        
        
def rate_movie(raw: RawRating, name: str) -> dict:
    score = raw.score
    if score > 5 or score < 1:
        return {
            "error": "Rating must be between 1 and 5"
        }
    rating = Rating(score=score)
    
    stmt = sa.select(Movie).where(Movie.name==name)
    
    with orm.Session(ENGINE) as session:
        movie = session.scalar(stmt)
        movie.ratings.append(rating)
        session.commit()
        
    return {
        "message": "The movie {name} has been given a rating of {score}"
    }

        
def rate_series(raw: RawRating, name: str) -> dict:
    score = raw.score
    if score > 5 or score < 1:
        return {
            "error": "Rating must be between 1 and 5"
        }
    rating = Rating(score=score)
    
    stmt = sa.select(Series).where(Series.name==name)
    
    with orm.Session(ENGINE) as session:
        series = session.scalar(stmt)
        series.ratings.append(rating)
        session.commit()
        
    return {
        "message": "The series {name} has been given a rating of {score}"
    }

        
def rate_episode(raw: RawRating, series_name: str, name: str) -> dict:
    score = raw.score
    if score > 5 or score < 1:
        return {
            "error": "Rating must be between 1 and 5"
        }
    rating = Rating(score=score)
    stmt = sa.select(Episode).where(Episode.name==name)
    
    with orm.Session(ENGINE) as session:
        episode = session.scalar(stmt)
        if episode.series.name == series_name:
            episode.ratings.append(rating)
            session.commit()
        else:
            return {
                "message": f"The episode '{name}' is not in the series '{series_name}'"
            }
        
    return {
        "message": "The episode {name} has been given a rating of {score}"
    }