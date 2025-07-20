import os
import json

from typing import List, Union, Optional
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
    
    
class RawMovie(BaseModel):
    name: str
    duration: int
    genres: List[str]
    
    
class UpdateMovie(BaseModel):
    name: Optional[str] = None
    duration: Optional[int] = None
    genres: Optional[List[str]] = None
    
    
class RawSeries(BaseModel):
    name: str
    genres: List[str]
    
    
class UpdateSeries(BaseModel):
    name: Optional[str] = None
    genres: Optional[List[str]] = None
    
    
class RawEpisode(BaseModel):
    name: str
    duration: int
    season: int
    genres: List[str]
    
    
class UpdateEpisode(BaseModel):
    name: Optional[str] = None
    duration: Optional[int] = None
    season: Optional[int] = None
    genres: Optional[List[str]] = None
    

class RawGenre(BaseModel):
    name: str


def show_movies(page: int = 1, size: int = 20) -> List[dict]:
    offset = (page - 1) * size
    stmt = sa.select(Movie).offset(offset).limit(size)
    with orm.Session(ENGINE) as session:
        movies = session.scalars(stmt)
        return [m.to_dict() for m in movies]
    
            
def show_series(page: int = 1, size: int = 20) -> List[dict]:
    offset = (page - 1) * size
    stmt = sa.select(Series).offset(offset).limit(size)
    with orm.Session(ENGINE) as session:
        series = session.scalars(stmt)
        return [s.to_dict() for s in series]
         
            
def show_all(page: int, size: int = 20) -> List[dict]:
    offset = (page - 1) * size
    stmt = (
        sa.select(Content)
        .where(sa.or_(Content.type=='movie', Content.type=='series'))
        .offset(offset)
        .limit(size)
    )
    with orm.Session(ENGINE) as session:
        contents = session.scalars(stmt)
        return [c.to_dict() for c in contents]
    
    
def show_genres() -> List[dict]:
    stmt = sa.select(Genre)
    
    with orm.Session(ENGINE) as session:
        genres = session.scalars(stmt)
        return [g.to_dict() for g in genres]


def show_movies_by_genre(name: str, page: int = 1, size: int = 20) -> List[dict]:
    offset = (page - 1) * size
    stmt = (
        sa.select(Content)
        .join(Genre.contents)
        .where(sa.and_(Genre.name == name, Content.type == "movie"))
        .order_by(Content.id)
        .offset(offset)
        .limit(size)
    )
    
    with orm.Session(ENGINE) as session:
        movies = session.scalars(stmt)
        return [m.to_dict() for m in movies]
          
            
def show_series_by_genre(name: str, page: int = 1, size: int = 20) -> List[dict]:
    offset = (page - 1) * size
    stmt = (
        sa.select(Content)
        .join(Genre.contents)
        .where(sa.and_(Genre.name == name, Content.type == "serie"))
        .order_by(Content.id)
        .offset(offset)
        .limit(size)
    )
    
    with orm.Session(ENGINE) as session:
        series = session.scalars(stmt)
        return [s.to_dict() for s in series]
            
            
def show_content_by_genre(name: str, page: int = 1, size: int = 20) -> List[dict]:
    offset = (page - 1) * size
    stmt = (
        sa.select(Content)
        .join(Genre.contents)
        .where(sa.and_(
            sa.or_(Content.type=='movie', Content.type=='series'),
            Genre.name == name
        ))
        .offset(offset)
        .limit(size)
    )
    with orm.Session(ENGINE) as session:
        contents = session.scalars(stmt)
        return [c.to_dict() for c in contents]
    
    
def show_eps_of_series(name: str, season: int = 0) -> Union[dict, List[dict]]:
    series_stmt = sa.select(Series).where(Series.name == name)

    with orm.Session(ENGINE) as session:
        series = session.scalar(series_stmt)
        if series and season == 0:
            return [ep.to_dict() for ep in series.episodes]
        elif series and season != 0:
            return [ep.to_dict() for ep in series.episodes if ep.season == season]
        else:
            return {
                "message": f"'{name}' is not a series"
            }
      

def find_content(name: str) -> dict:
    stmt = sa.select(Content).where(Content.name == name)
    
    with orm.Session(ENGINE) as session:
        content = session.scalar(stmt)
        if content:
            return content.to_dict()
        else:
            return {
                "message": f"'{name}' not found in Movies"
            }
    

def find_movie(name: str) -> dict:
    stmt = sa.select(Movie).where(Movie.name == name)
    
    with orm.Session(ENGINE) as session:
        movie = session.scalar(stmt)
        if movie:
            return movie.to_dict()
        else:
            return {
                "message": f"'{name}' not found in movies"
            }
            
            
def find_series(name: str) -> dict:
    stmt = sa.select(Series).where(Series.name == name)
    
    with orm.Session(ENGINE) as session:
        series = session.scalar(stmt)
        if series:
            return series.to_dict()
        else:
            return {
                "message": f"'{name}' not found in series"
            }
            
            
def find_episode(name: str, series_name: str) -> dict:
    stmt = sa.select(Episode).where(Episode.name == name)
    
    with orm.Session(ENGINE) as session:
        ep = session.scalar(stmt)
        if ep and ep.series.name == series_name:
            return ep.to_dict()
        else:
            return {
                "messages": f"'{name}' not found in the episodes of the series: '{series_name}'"
            }
            
            
def find_genre(name: str) -> dict:
    stmt = sa.select(Genre).where(Genre.name == name)
    
    with orm.Session(ENGINE) as session:
        g = session.scalar(stmt)
        if g:
            return g.to_dict()
        else:
            return {"messages": f"Genre '{name}' not found"}
        
        
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
        "message": f"The movie '{name}' has been given a rating of {score}"
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
        "message": f"The series '{name}' has been given a rating of {score}"
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
        "message": f"The episode '{name}' has been given a rating of {score}"
    }
    
def add_movie(raw: RawMovie):
    m = Movie(name=raw.name, duration=raw.duration)
    gnr_stmt = sa.select(Genre).filter(Genre.name.in_(raw.genres))
    message = ""
    
    with orm.Session(ENGINE) as session:
        genres = session.scalars(gnr_stmt)
        if genres:
            m.genres.extend(genres)
        else:
            message = f"Genres '{genres}' not found. Adding movie '{raw.name}' anyway"
        session.add(m)
        session.commit()
        
    if not message:
        return {"message": f"The movie '{raw.name}' has been added"}
    else:
        return {"message": message}
    
    
def add_series(raw: RawSeries):
    s = Series(name=raw.name)
    gnr_stmt = sa.select(Genre).filter(Genre.name.in_(raw.genres))
    message = ""
    
    with orm.Session(ENGINE) as session:
        genres = session.scalars(gnr_stmt)
        if genres:
            s.genres.extend(genres)
        else:
            message = f"Genres '{genres}' not found. Adding series '{raw.name}' anyway"
        session.add(s)
        session.commit()
        
    if not message:
        return {"message": f"The series '{raw.name}' has been added"}
    else:
        return {"message": message}
    
    
def add_episode(raw: RawEpisode, series_name: str):
    ep = Episode(name=raw.name, duration=raw.duration, season=raw.season)
    series_stmt = (
        sa.select(Series)
        .where(Series.name == series_name)
        .order_by(Series.id)
        .limit(1)
    )
    
    with orm.Session(ENGINE) as session:
        s = session.scalar(series_stmt)
        if s:
            ep.genres = s.genres
            s.episodes.append(ep)
            session.commit()
        else:
            return {"message": f"The series '{series_name}' wasn't found"}
        
    return {
        "message": f"The episode '{raw.name}' has been added to '{series_name}'"
    }
    

def add_genre(raw: RawGenre):
    g = Genre(name=raw.name)
    with orm.Session(ENGINE) as session:
        session.add(g)
        session.commit()
        
    return {"message": f"The genre '{raw.name}' has been added"}
    

def remove_movie(name: str) -> dict:
    stmt = sa.select(Movie).where(Movie.name == name).order_by(Movie.id).limit(1)
    
    with orm.Session(ENGINE) as session:
        movie = session.scalar(stmt)
        if movie:
            session.delete(movie)
            session.commit()
        else:
            return {
                "message": f"'{name}' not found in movies"
            }
            
    return {"message": f"Movie '{name}' has been deleted"}
            
            
def remove_series(name: str) -> dict:
    stmt = sa.select(Series).where(Series.name == name).order_by(Series.id).limit(1)
    
    with orm.Session(ENGINE) as session:
        series = session.scalar(stmt)
        if series:
            session.delete(series)
            session.commit()
        else:
            return {
                "message": f"'{name}' not found in series"
            }
            
    return {"message": f"Series '{name}' has been deleted"}
            
            
def remove_episode(name: str, series_name: str) -> dict:
    stmt = sa.select(Episode).where(Episode.name == name).order_by(Episode.id).limit(1)
    
    with orm.Session(ENGINE) as session:
        ep = session.scalar(stmt)
        if ep and ep.series.name == series_name:
            session.delete(ep)
            session.commit()
        else:
            return {
                "messages": f"'{name}' not found in the episodes of the series: '{series_name}'"
            }
            
    return {
        "message": f"Episode '{name}' has beend deleted from series '{series_name}'"
    }
    
    
def remove_genre(name: str) -> dict:
    stmt = sa.select(Genre).where(Genre.name == name).order_by(Genre.id).limit(1)
    
    with orm.Session(ENGINE) as session:
        g = session.scalar(stmt)
        if g:
            session.delete(g)
            session.commit()
        else:
            return {
                "messages": f"'{name}' not found in the catalog genres"
            }
            
    return {"message": f"Genre '{name}' has been deleted"}


def update_movie(name: str, raw: UpdateMovie) -> dict:
    stmt = sa.select(Movie).where(Movie.name == name).order_by(Movie.id).limit(1)
    
    with orm.Session(ENGINE) as session:
        m = session.scalar(stmt)
        if m:
            update_data = raw.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(m, key, value)
            session.commit()
        else:
            return {"message": f"Movie '{name}' not found"}
        
    return {"message": f"Movie '{name}' has been updated"}


def update_series(name: str, raw: UpdateSeries) -> dict:
    stmt = sa.select(Series).where(Series.name == name).order_by(Series.id).limit(1)
    
    with orm.Session(ENGINE) as session:
        s = session.scalar(stmt)
        if s:
            update_data = raw.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(s, key, value)
            session.commit()
        else:
            return {"message": f"Series '{name}' not found"}
        
    return {"message": f"Series '{name}' has been updated"}


def update_episode(series_name: str, name: str, raw: UpdateEpisode) -> dict:
    stmt = (
        sa.select(Episode)
        .where(Episode.name == name)
        .order_by(Episode.id)
        .limit(1)
    )
    
    with orm.Session(ENGINE) as session:
        ep = session.scalar(stmt)
        if ep and ep.series.name == series_name:
            update_data = raw.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(ep, key, value)
            session.commit()
        else:
            return {"message": f"Episode '{name}' not found in series '{series_name}'"}

    return {"message": f"Episode '{name}' in series '{series_name}' has been updated"}


def update_genre(name: str, raw: RawGenre) -> dict:
    stmt = sa.select(Genre).where(Genre.name == name).order_by(Genre.id).limit(1)
    
    with orm.Session(ENGINE) as session:
        g = session.scalar(stmt)
        if g:
            update_data = raw.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(g, key, value)
            session.commit()
        else:
            return {"message": f"Genre '{name}' not found"}
        
    return {"message": f"Genre '{name}' has been updated"}