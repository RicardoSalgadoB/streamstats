import os
import json

from typing import List, Union, Optional
from pydantic import BaseModel
from dotenv import load_dotenv

import sqlalchemy as sa
import sqlalchemy.orm as orm

from fastapi import HTTPException

from app.models import Content, Movie, Episode, Series, Genre, Rating

# Load DB URL
load_dotenv()
db_url = os.getenv("DB_URL")

# Create Engine for SQLAlchemy
ENGINE = sa.create_engine(db_url)

# CLASSES FOR API METHODS #
    # Class for posts/creating rows
class RawRating(BaseModel):
    score: int
    
    # Class for posts/creating rows
class RawMovie(BaseModel):
    name: str
    duration: int
    genres: List[str]
    
    
    # Class for patches/updating rows
class UpdateMovie(BaseModel):
    name: Optional[str] = None
    duration: Optional[int] = None
    genres: Optional[List[str]] = None
    
    
    # Class for patches/updating rows
class RawSeries(BaseModel):
    name: str
    genres: List[str]
    
    
    # Class for patches/updating rows
class UpdateSeries(BaseModel):
    name: Optional[str] = None
    genres: Optional[List[str]] = None
    
    
    # Class for patches/updating rows
class RawEpisode(BaseModel):
    name: str
    duration: int
    season: int
    genres: List[str]
    
    
    # Class for patches/updating rows
class UpdateEpisode(BaseModel):
    name: Optional[str] = None
    duration: Optional[int] = None
    season: Optional[int] = None
    genres: Optional[List[str]] = None
    

    # Class for patches/updating rows
class RawGenre(BaseModel):
    name: str

# SHOWING METHODS #

def show_movies(page: int = 1, size: int = 20) -> List[dict]:
    """Show all movies in a paginated manner for performance reasons.

    Args:
        page (int, optional): Number of the page shown. Defaults to 1.
        size (int, optional): How many results are going to be shown in each page. Defaults to 20.

    Returns:
        List[dict]: If failure return a message, if not return a list movie dictionaries.
    """
    offset = (page - 1) * size  # Calculate offset from page and size
    stmt = sa.select(Movie).offset(offset).limit(size)  # Prepare statement
    with orm.Session(ENGINE) as session:
        movies = session.scalars(stmt)  # execute statement
        if movies:
            return [m.to_dict() for m in movies]    # no need to commit only looking around
        else:
            raise HTTPException(status_code=404, detail="No movies in the database. Add one.")
    
            
def show_series(page: int = 1, size: int = 20) -> List[dict]:
    """Show all series in a paginated manner for performance reasons.

    Args:
        page (int, optional): Number of the page shown. Defaults to 1. Passed as query parameter.
        size (int, optional): How many results are going to be shown in each page. Defaults to 20. Passed as query parameter.

    Returns:
        List[dict]: If failure return a message, if not return a list series dictionaries.
    """
    offset = (page - 1) * size 
    stmt = sa.select(Series).offset(offset).limit(size)
    with orm.Session(ENGINE) as session:
        series = session.scalars(stmt)
        if series:
            return [s.to_dict() for s in series]
        else:
            raise HTTPException(status_code=404, detail="No series in the database. Add one.")
        
            
def show_all(page: int = 1, size: int = 20) -> List[dict]:
    """Show both all series and all movies in a paginated manner for performance reasons.

    Args:
        page (int, optional): Number of the page shown. Defaults to 1. Passed as query parameter,
        size (int, optional): How many results are going to be shown in each page. Defaults to 20. Passed as query parameter,

    Returns:
        List[dict]: If failure raises exception, if not return a list series dictionaries.
    """
    offset = (page - 1) * size
    stmt = (
        sa.select(Content)
        .where(sa.or_(Content.type=='movie', Content.type=='series'))
        .offset(offset)
        .limit(size)
    )
    with orm.Session(ENGINE) as session:
        contents = session.scalars(stmt)
        if contents:
            return [c.to_dict() for c in contents]
        else:
            raise HTTPException(status_code=404, detail="No movies or series in the database. Add one.")
    
    
def show_genres() -> List[dict]:
    """Show all genre dictionaries in the database.

    Returns:
        List[dict]: In failure raises exception. If not return the genre dicitonaries.
    """
    stmt = sa.select(Genre)
    with orm.Session(ENGINE) as session:
        genres = session.scalars(stmt)
        if genres:
            return [g.to_dict() for g in genres]
        else:
            raise HTTPException(status_code=404, detail="No genres in the catalog. Add one.")


def show_movies_by_genre(name: str, page: int = 1, size: int = 20) -> List[dict]:
    """Show all movies that belong to a given genre in pages/chunks.

    Args:
        name (str): Name of the genre. Passed as path parameter.
        page (int, optional): Number of the page shown. Defaults to 1. Passed as query parameter.
        size (int, optional): How many results are going to be shown in each page. Passed as query parameter.
            Defaults to 20.

    Returns:
        List[dict]: 
            Success: Returns the list of the movie dicts of the given genre.
    """
    offset = (page - 1) * size
    stmt = (
        sa.select(Content)
        .join(Genre.contents)   # Use content instead of movie because of this line
        .where(sa.and_(Genre.name == name, Content.type == "movie"))
        .order_by(Content.id)
        .offset(offset)
        .limit(size)
    )
    
    with orm.Session(ENGINE) as session:
        movies = session.scalars(stmt)
        if movies:
            return [m.to_dict() for m in movies]
        else:
            raise HTTPException(status_code=404, detail=f"No movies in genre '{name}'. Add one.")
          
            
def show_series_by_genre(name: str, page: int = 1, size: int = 20) -> List[dict]:
    """Show all series that belong to a given genre in paginated way.

    Args:
        name (str): Name of the genre. Passed as path parameter.
        page (int, optional): Number of the page shown. Defaults to 1. Passed as query parameter.
        size (int, optional): How many results are going to be shown in each page. Passed as query parameter.
            Defaults to 20.

    Returns:
        List[dict]: 
            Success: Returns the list of the movie dicts of the given genre.
    """
    offset = (page - 1) * size
    stmt = (
        sa.select(Content)
        .join(Genre.contents)   # Use content instead of series because of this line
        .where(sa.and_(Genre.name == name, Content.type == "serie"))
        .order_by(Content.id)
        .offset(offset)
        .limit(size)
    )
    
    with orm.Session(ENGINE) as session:
        series = session.scalars(stmt)
        if series:
            return [s.to_dict() for s in series]
        else:
            raise HTTPException(status_code=404, detail=f"No series in genre '{name}'. Add one.")

            
def show_content_by_genre(name: str, page: int = 1, size: int = 20) -> List[dict]:
    """Show both that belong to a given genre in paginated way.

    Args:
        name (str): Name of the genre. Passed as path parameter.
        page (int, optional): Number of the page shown. Defaults to 1. Passed as query parameter
        size (int, optional): How many results are going to be shown in each page. Passed as query parameter.
            Defaults to 20.

    Returns:
        List[dict]: 
            Success: Returns the list of the content dicts of the given genre.
    """
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
        if contents:
            return [c.to_dict() for c in contents]
        else:
            raise HTTPException(status_code=404, detail=f"No series in genre '{name}'. Add one.")
    
    
def show_eps_of_series(name: str, season: int = 0) -> List[dict]:
    """Show all the episodes that are in a series (optinally, in a given season).

    Args:
        name (str): Name of the series. Passed as path parameter.
        season (int, optional): Number of the season to be shown. Defaults to 0, if so it is ignored. Passed as query parameter

    Returns:
        List[dict]:
            Success: A list of the episodes of the series (can be empty).
    """
    series_stmt = sa.select(Series).where(Series.name == name)

    with orm.Session(ENGINE) as session:
        series = session.scalar(series_stmt)
        if series and season == 0:
            return [ep.to_dict() for ep in series.episodes]
        elif series and season != 0:
            return [ep.to_dict() for ep in series.episodes if ep.season == season]
        else:
            raise HTTPException(status_code=404, detail=f"'{name}' is not a series")
      

# FINDING METHODS #

def find_content(name: str) -> dict:
    """A funciton to find any ONE specific movie, series or episodes.

    Args:
        name (str): The name of the content that wants to be found. Passed as path parameter.

    Returns:
        dict: A dictionary of the desired content.
    """
    stmt = sa.select(Content).where(Content.name == name).order_by(Content.id).limit(1)
        # If multiple with the same name, just pick the one with the smallest id
        
    with orm.Session(ENGINE) as session:
        content = session.scalar(stmt)
        if content:
            return content.to_dict()
        else:
            raise HTTPException(status_code=404, detail=f"'{name}' not found in Movies, Series or Episodes")
    

def find_movie(name: str) -> dict:
    """Finds ONE specific movie.

    Args:
        name (str): The name of the movie. This is a path parameter.

    Returns:
        dict: A dictinary of the movie.
    """
    stmt = sa.select(Movie).where(Movie.name == name).order_by(Movie.id).limit(1)
        # Same as above
    
    with orm.Session(ENGINE) as session:
        movie = session.scalar(stmt)
        if movie:
            return movie.to_dict()
        else:
            raise HTTPException(status_code=404, detail=f"'{name}' not found in Movies")
            
            
def find_series(name: str) -> dict:
    """Finds ONE specific series (if multiple names, the one with the smallest id.)

    Args:
        name (str): Name of the series to be found. Passed as path parameter.

    Returns:
        dict: The dictionary of the series
    """
    stmt = sa.select(Series).where(Series.name == name).order_by(Series.id).limit(1)
    
    with orm.Session(ENGINE) as session:
        series = session.scalar(stmt)
        if series:
            return series.to_dict()
        else:
            raise HTTPException(status_code=404, detail=f"'{name}' not found in Series")
            
            
def find_episode(name: str, series_name: str) -> dict:
    """Find one episode that belongs to a given series.

    Args:
        name (str): The name of the episodes. Passed as path parameter.
        series_name (str): The name of the series. Passed as path parameter.

    Returns:
        dict: The ep dict if found.
    """
    stmt = sa.select(Episode).where(Episode.name == name)
    
    with orm.Session(ENGINE) as session:
        eps = session.scalars(stmt)
        for ep in eps:  # If there are multiple episodes with the same name
            if ep and ep.series.name == series_name:
                    # Check everyone of them to see if it is in the given series
                return ep.to_dict()

        # This is still technically true even if the episode doesn't exist
        raise HTTPException(status_code=404, detail=f"'{name}' not found in the Episodes of the series: '{series_name}'")
            
            
def find_genre(name: str) -> dict:
    """Find a given genre.

    Args:
        name (str): The name of the genre. This is a path paramenter.

    Returns:
        dict: Either the dict of the genre or a message if not found.
    """
    stmt = sa.select(Genre).where(Genre.name == name)
        # Genre name is unique, so no need for limit
    
    with orm.Session(ENGINE) as session:
        g = session.scalar(stmt)
        if g:
            return g.to_dict()
        else:
            raise HTTPException(status_code=404, detail=f"Genre '{name}' not found")


# RATING METHODS # 
        
def rate_movie(raw: RawRating, name: str) -> dict:
    """Funciton to add a user rating to a movie.

    Args:
        raw (RawRating): The json payload from the function parsed as Pydantic Base Model.
        name (str): Name of the movie. Path parameter.

    Returns:
        dict: Message indicating success.
    """
    score = raw.score
    if score > 5 or score < 1:
        return {
            "error": "Rating must be between 1 and 5"
        }
    rating = Rating(score=score)
    
    stmt = sa.select(Movie).where(Movie.name==name).order_by(Movie.id).limit(1)
        # If there are movies that share a name
    
    with orm.Session(ENGINE) as session:
        movie = session.scalar(stmt)
        if movie:
            movie.ratings.append(rating)
            session.commit()
        else:
            raise HTTPException(status_code=404, detail=f"Movie '{name}' not found.")
        
    return {
        "message": f"The movie '{name}' has been given a rating of {score}"
    }

        
def rate_series(raw: RawRating, name: str) -> dict:
    """Adds a user rating to a given series.

    Args:
        raw (RawRating): Json Payload parse as pydantic model.
        name (str): Name of the series. Path paramenter.

    Returns:
        dict: A message indicationg sucess.
    """
    score = raw.score
    if score > 5 or score < 1:
        return {
            "error": "Rating must be between 1 and 5"
        }
    rating = Rating(score=score)
    
    stmt = sa.select(Series).where(Series.name==name)
    
    with orm.Session(ENGINE) as session:
        series = session.scalar(stmt)
        if series:
            series.ratings.append(rating)
            session.commit()
        else:
            raise HTTPException(status_code=404, detail=f"Series '{name}' not found.")
        
    return {
        "message": f"The series '{name}' has been given a rating of {score}"
    }

        
def rate_episode(raw: RawRating, series_name: str, name: str) -> dict:
    """Adds a user ratings to a given episodes

    Args:
        raw (RawRating): Parsed Json payload.
        series_name (str): Name of the series. Path parameter.
        name (str): Name of the Episode. Path parameter.

    Returns:
        dict: A message indicating success.
    """
    score = raw.score
    if score > 5 or score < 1:
        return {
            "error": "Rating must be between 1 and 5"
        }
    rating = Rating(score=score)
    stmt = sa.select(Episode).where(Episode.name==name)
    
    with orm.Session(ENGINE) as session:
        eps = session.scalars(stmt) # If many eps with same name
        for ep in eps:  # Check if each ep is in the series
            if ep.series.name == series_name:   # if so add the rating.
                ep.ratings.append(rating)
                session.commit()    
                return {
                    "message": f"The episode '{name}' has been given a rating of {score}"
                }
    
    raise HTTPException(status_code=404, detail=f"The episode '{name}' is not in the series '{series_name}'")


# ADDING METHODS #
    
def add_movie(raw: RawMovie) -> dict:
    """Adds a movie to the catalog.

    Args:
        raw (RawMovie): Parsed JSON payload.

    Returns:
        dict: A message telling the user the movie was added (with or without genres)
    """
    m = Movie(name=raw.name, duration=raw.duration) # Create the movie object
    gnr_stmt = sa.select(Genre).filter(Genre.name.in_(raw.genres))  # Check if the given genre is already created.
    message = ""
    
    with orm.Session(ENGINE) as session:
        genres = session.scalars(gnr_stmt)
        if genres:  # if the genres are found, add them to the movie object.
            m.genres.extend(genres)
        else:   # the admin has to create each genre manually
            message = f"Genres '{genres}' not found. Adding movie '{raw.name}' anyway"
        session.add(m)
        session.commit()
        
    if not message:
        return {"message": f"The movie '{raw.name}' has been added"}
    else:
        return {"message": message}
    
    
def add_series(raw: RawSeries) -> dict:
    """Add a series row to the catalog.

    Args:
        raw (RawSeries): Parsed JSON payload.

    Returns:
        dict: A message indicating if the series was added with or without genres.
    """
    s = Series(name=raw.name)   # Create series object
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
    
    
def add_episode(raw: RawEpisode, series_name: str) -> dict:
    """Add an episode to a series.

    Args:
        raw (RawEpisode): Parsed JSON payload.
        series_name (str): Name of the Series. Path parameter.

    Returns:
        dict: A message indicating success.
    """
    ep = Episode(name=raw.name, duration=raw.duration, season=raw.season)
    series_stmt = (
        sa.select(Series)
        .where(Series.name == series_name)
        .order_by(Series.id)
        .limit(1)
    )
    # Only select the series with the smallest id if many series with the same name.
    
    with orm.Session(ENGINE) as session:
        s = session.scalar(series_stmt)
        if s:
            ep.genres = s.genres
            s.episodes.append(ep)
            session.commit()
        else:
            raise HTTPException(status_code=404, detail=f"The series '{series_name}' wasn't found")
        
    return {
        "message": f"The episode '{raw.name}' has been added to '{series_name}'"
    }
    

def add_genre(raw: RawGenre) -> dict:
    """Add a genre to the catalog.

    Args:
        raw (RawGenre): Parsed JSON payload.

    Returns:
        dict: A meesage indicating the genre has been added.
    """
    stmt = sa.select(sa.func.count()).select_from(Genre).filter(Genre.name == raw.name)
        # Count to check if the genre already exists
    with orm.Session(ENGINE) as session:
        count = session.scalar(stmt)
        if count == 0:  # If the genre doesn't already exist. Create it and add it.
            g = Genre(name=raw.name)
            session.add(g)
            session.commit()
        else:   # If it already exists tell the user
            HTTPException(status_code=400, detail=f"The genre '{raw.name}' already exists")
        
    return {"message": f"The genre '{raw.name}' has been added"}
 

# REMOVING METHODS #   

def remove_movie(name: str) -> dict:
    """Function to remove a movie from the catalog.

    Args:
        name (str): The name of the movie to be deleted. Path parameter.

    Returns:
        dict: A message indicating the movie has been deleted.
    """
    stmt = sa.select(Movie).where(Movie.name == name).order_by(Movie.id).limit(1)
        # limit to only the top result

    with orm.Session(ENGINE) as session:
        movie = session.scalar(stmt)
        if movie:
            session.delete(movie)
            session.commit()
        else:
            raise HTTPException(status_code=404, detail=f"'{name}' not found in movies")
            
    return {"message": f"Movie '{name}' has been deleted"}
            
            
def remove_series(name: str) -> dict:
    """Removes a series from the catalog.

    Args:
        name (str): The name of the series to be removed. Path parameter.

    Returns:
        dict: A message indicating a succesful deletion.
    """
    stmt = sa.select(Series).where(Series.name == name).order_by(Series.id).limit(1)
    
    with orm.Session(ENGINE) as session:
        series = session.scalar(stmt)
        if series:
            session.delete(series)
            session.commit()
        else:
            raise HTTPException(status_code=404, detail=f"'{name}' not found in series")
            
    return {"message": f"Series '{name}' has been deleted"}
            
            
def remove_episode(name: str, series_name: str) -> dict:
    """Removes an episode from the database.

    Args:
        name (str): Name of the episode to be removed. Path paramenter.
        series_name (str): Name of the series in which the episode belongs. Path parameter.

    Returns:
        dict: Message indicating a succesfule deletion if so.
    """
    stmt = sa.select(Episode).where(Episode.name == name).order_by(Episode.id).limit(1)
    
    with orm.Session(ENGINE) as session:
        ep = session.scalar(stmt)
        if ep and ep.series.name == series_name:
            session.delete(ep)
            session.commit()
        else:
            raise HTTPException(status_code=404, detail=f"'{name}' not found in the episodes of the series: '{series_name}'")
            
    return {
        "message": f"Episode '{name}' has been deleted from series '{series_name}'"
    }
    
    
def remove_genre(name: str) -> dict:
    """Removes a given genre from the catalog.

    Args:
        name (str): The name of the genre

    Returns:
        dict: Message indicating a successfult deletion if so
    """
    stmt = sa.select(Genre).where(Genre.name == name)   # name is unique
    
    with orm.Session(ENGINE) as session:
        g = session.scalar(stmt)
        if g:
            session.delete(g)
            session.commit()
        else:
            raise HTTPException(status_code=404, detail=f"'{name}' not found in the catalog genres")
            
    return {"message": f"Genre '{name}' has been deleted"}


# UPDATING METHODS #

def update_movie(raw: UpdateMovie, name: str) -> dict:
    """Update a movie object, any of its attributes can be changed.

    Args:
        raw (UpdateMovie): Parsed JSON object (include any attributes to be changed, check examples)
        name (str): Actual (Old) Name of the movie. Path parameter.

    Returns:
        dict: Message indicating update.
    """
    stmt = sa.select(Movie).where(Movie.name == name).order_by(Movie.id).limit(1)
    
    with orm.Session(ENGINE) as session:
        m = session.scalar(stmt)
        if m:
            update_data = raw.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(m, key, value)
            session.commit()
        else:
            raise HTTPException(status_code=404, detail=f"Movie '{name}' not found")
        
    return {"message": f"Movie '{name}' has been updated"}


def update_series(raw: UpdateSeries, name: str) -> dict:
    """Update any attributes of series object in the catalog.

    Args:
        raw (UpdateSeries): Parsed JSON payload as pydantic Base Model with new attributes.
        name (str): Actual (old) Name of the series. Path parameter.

    Returns:
        dict: A message indicating a successful update.
    """
    stmt = sa.select(Series).where(Series.name == name).order_by(Series.id).limit(1)
    
    with orm.Session(ENGINE) as session:
        s = session.scalar(stmt)
        if s:
            # dump the json payload into a dictionary
            update_data = raw.model_dump(exclude_unset=True)
            # iterate through the dicitnary updating the given attributes.
            for key, value in update_data.items():
                setattr(s, key, value)
            session.commit()
        else:
            raise HTTPException(status_code=404, detail= f"Series '{name}' not found")
        
    return {"message": f"Series '{name}' has been updated"}


def update_episode(raw: UpdateEpisode, name: str, series_name: str) -> dict:
    """Updates the attributes of an episode in a given series.

    Args:
        raw (UpdateEpisode): Parsed JSON Payload with new attributes.
        name (str): Actual (old) Name of the Episode. Path parameter.
        series_name (str): Name of the Series. Path parameter.

    Returns:
        dict: A message indicating a successful update.
    """
    stmt = (
        sa.select(Episode)
        .where(Episode.name == name)
        .order_by(Episode.id)
        .limit(1)
    )
    
    with orm.Session(ENGINE) as session:
        ep = session.scalar(stmt)
        if ep and ep.series.name == series_name:
            # get request into dict
            update_data = raw.model_dump(exclude_unset=True)
            # iterate through the dict updating where necessary
            for key, value in update_data.items():
                setattr(ep, key, value)
            session.commit()
        else:
            raise HTTPException(status_code=404, detail=f"Episode '{name}' not found in series '{series_name}'")

    return {"message": f"Episode '{name}' in series '{series_name}' has been updated"}


def update_genre(raw: RawGenre, name: str) -> dict:
    """Updates teh attributes (name) of genre in the catalog.

    Args:
        raw (RawGenre): Parsed JSON payload with the replacements.
        name (str): Actual (Old) name of the genre

    Returns:
        dict: A message indicating a succesful response.
    """
    stmt = sa.select(Genre).where(Genre.name == name).order_by(Genre.id).limit(1)
    
    with orm.Session(ENGINE) as session:
        g = session.scalar(stmt)
        if g:
            # same as above
            update_data = raw.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(g, key, value)
            session.commit()
        else:
            raise HTTPException(status_code=404, detail=f"Genre '{name}' not found")
        
    return {"message": f"Genre '{name}' has been updated"}