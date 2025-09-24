import pandas as pd
import numpy as np
from typing import List

from extract import main_extract

# Dictionary with the translations from spanish to english
TRANSLATIONS = {
    'A tope': 'Adrenaline Rush',
    'Sobredosis de Adrenalina': 'Adrenaline Rush',
    'Hacia lo desconocido': 'Into the Unknown',
    'Mucha Risa': 'Comedy Gold',
    'Viaje Emocional': 'Emotional Journey',
    'Dimensión Emocional': 'Emotional Journey',
    'El surgimiento de los muertos': 'Blood Moon Rising',
    'El Acenso de la luna roja': 'Blood Moon Rising',
    'El Ascenso del Mal': 'Blood Moon Rising',
    'La Hora Final': 'The Final Hour',
    'La Última Hora': 'The Final Hour',
    'La Historia del Perro de Abajo': 'The Underdog Story'
}

# Declare nonfiction genres to be removed
NON_FICTION_GENRES = ["Documentary", "Reality"]

# Genres that are to be renamed for better analysis
GENRE_TRANSFORMATIONS = {
    "Sci-Fi": ["Science", "Fiction"],
    "Science_Fiction": ["Science", "Fiction"],
    "CGI": ["3D"],
    "Traditional 2D" : ["2D"],
    "Romantic Comedy": ["Romance", "Comedy"],
    "Family Drama": ["Family", "Drama"],
    "Psychological Drama": ["Psychological", "Drama"],
    "Social Drama": ["Social", "Drama"],
    "Political Drama": ["Political", "Drama"],
    "Criminal Drama": ["Criminal", "Drama"],
    "Legal Drama": ["Legal", "Drama"],
    "Medical Drama": ["Medical", "Drama"],
    "Psychological Horror": ["Psychological", "Horror"],
    "Dance Musical": ["Dance", "Musical"],
    "Biographical Musical": ["Biographical", "Musical"],
    "Historical Romance": ["Historical", "Romance"],
    "Contemporary Romance": ["Contemporary", "Romance"],
    "Paranormal Romance": ["Paranormal", "Romance"],
    "Erotic Romance": ["Erotic", "Romance"],
    "Science Fantasy": ["Science", "Fantasy"],
    "Psychological Thriller": ["Psychological", "Thriller"],
    "Political Thriller": ["Political", "Thriller"],
    "Techno Thriller": ["Techno", "Thriller"],
    "Medical Thriller": ["Medical", "Thriller"],
    "Legal Thriller": ["Legal", "Thriller"],
    "Conspiracy Thriller": ["Conspiracy", "Thriller"],
    "Comedy Western": ["Comedy", "Western"],
    "Space Western": ["Science Fiction", "Western"],
}


def theManagement(df: pd.DataFrame):
    titles = df["title"].to_list()
    for title in titles:
        title_with_the = "The " + title
        title_with_the_exists = (df["title"] == title)
        if title_with_the_exists.any():
            df.loc[df["title"] == title, "title"] = title_with_the
            
            
def modifySeriesDuration(df_series: pd.DataFrame, df_episodes: pd.DataFrame):
    series_id_duration = df_episodes.groupby(["series_id"]).agg({"duration_minutes": "sum"})
    df_series = pd.merge(df_series, series_id_duration, left_index=True, right_index=True)
    df_series.drop(["duration_minutes_x"], inplace=True)
    df_series.rename({"duration_minutes_x":"duration_minutes"}, inplace=True)
    return df_series
    

def cleanData(
    df_movies: pd.DataFrame, 
    df_series: pd.DataFrame, 
    df_episodes: pd.DataFrame
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    # 1) Remove trailing or leading blankspaces
    df_movies["title"] = df_movies["title"].apply(lambda s: s.strip(' '))
    df_series["title"] = df_series["title"].apply(lambda s: s.strip(' '))
    df_episodes["title"] = df_episodes["title"].apply(lambda s: s.strip(' '))
    
    # 2) Deal with the "The"
    theManagement(df_movies)    # function could also be "theDealer"
    theManagement(df_series)
    theManagement(df_episodes)
    
    # 3) Translate back titles from Spanish to English
    for spanish, english in TRANSLATIONS:
        df_movies.loc[df_movies["title"] == spanish, "title"] = english
        df_series.loc[df_series["title"] == spanish, "title"] = english
        df_episodes.loc[df_episodes["title"] == spanish, "title"] = english
        
    # 4) Standarize length in minutes
        # movies
    movie_threshold = 245
    df_movies.loc[
        df_movies["duration_minutes"] > movie_threshold,
        "duration_minutes"
    ] = df_movies["duration_minutes"]/60
    
        # episodes
    episode_threshold = 119
    df_episodes.loc[
        df_episodes["duration_minutes"] > episode_threshold,
        "duration_minutes"
    ] = df_episodes["duration_minutes"]/60
    
        # series
    modifySeriesDuration(df_series, df_episodes)
    
    # Return dataframes
    return df_movies, df_series, df_episodes


def transformGenres(genres: List[str]):
    res = set()
    
    for g in genres:
        new_genres = [g] if g in GENRE_TRANSFORMATIONS else GENRE_TRANSFORMATIONS[g]
        for gen in new_genres:
            res.add(gen)
            
    return list(res)


def createGenreHierarchy(
    df_movies: pd.DataFrame, 
    df_series: pd.DataFrame, 
    df_episodes: pd.DataFrame
):
    # Amount of time the genre appears overall
    genre_count = {}
    
    # Count genres on movies
    for genres in df_movies["genres"]:
        for g in genres:
            if g in genre_count:
                genre_count[g] += 1
            else:
                genre_count[g] = 1
                
    pass

def addEpisodesToSeries(
    df_series: pd.DataFrame, 
    df_episodes: pd.DataFrame
) -> pd.DataFrame:
    episodes_by_series_id = df_episodes.groupby("series_id")["title"].agg(list)
    episodes_by_series_id.rename({"title":"episodes"})
    df_series = pd.merge(df_series, episodes_by_series_id, left_index=True, right_index=True)
    return df_series


def countGenreByCategory(
    df_movies: pd.DataFrame,
    df_series: pd.DataFrame
) -> dict:
    # Count genres on movies
    genre_movies = {}
    for genres in df_movies["genres"]:
        for g in genres:
            if g in genre_movies:
                genre_movies[g] += 1
            else:
                genre_movies[g] = 1
                
    # Count genres on series (episodes are the same proportion as series, so no need to count them)
    genre_series = {}
    for genres in df_series["genres"]:
        for g in genres:
            if g in genre_series:
                genre_series[g] += 1
            else:
                genre_series[g] = 1
                
    return {
        "movies": genre_movies,
        "series": genre_series
    }
    

def pdTransform(movies: dict, series: dict, episodes: dict):
    df_movies = pd.DataFrame(movies)
    df_movies.set_index("id", inplace=True)
    df_series = pd.DataFrame(series)
    df_series.set_index("id", inplace=True)
    df_episodes = pd.DataFrame(episodes)
    df_episodes.set_index("id", inplace=True)
    
    # I) Clean data
    df_movies, df_series, df_episodes = cleanData(df_movies, df_series, df_episodes)
    
    # II) Remove non fiction genres
    for genre in NON_FICTION_GENRES:
        df_movies.drop(
            index=df_movies[df_movies["genres"].apply(lambda g: genre in g)].index,
            inplace=True
        )
        df_series.drop(
            index=df_series[df_series["genres"].apply(lambda g: genre in g)].index,
            inplace=True
        )
        df_episodes.drop(
            index=df_episodes[df_episodes["genres"].apply(lambda g: genre in g)].index,
            inplace=True
        )
        
    # III) Process Genres
        # 1) Remove, Combine & Split Genres
    df_movies["genre"] = df_movies["genre"].apply(transformGenres)
    df_series["genre"] = df_series["genre"].apply(transformGenres)
    df_episodes["genre"] = df_episodes["genre"].apply(transformGenres)
    
        # 2) Genre Hierarchy
    
    # IV) Add Episodes to Series
    df_series = addEpisodesToSeries(df_series, df_episodes)
    
    # V) Count Movies, Series and Episodes in each genre
    genre_count = countGenreByCategory(df_movies, df_series)
    
    return df_movies, df_series, df_episodes, genre_count


if __name__ == '__main__':
    movies, series, episodes = main_extract()
    pdTransform(movies, series, episodes)    