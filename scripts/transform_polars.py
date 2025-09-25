import polars as pl
from typing import List
from extract import main_extract
from time import time

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


def theDealer(df: pl.DataFrame) -> pl.DataFrame:
    title_with_the_exists = pl.when(
        (pl.col("title").map_elements(lambda t: "The " + t)
         .is_in(pl.col("title")))
    )
    df = df.with_columns(
        title_with_the_exists
        .then(pl.lit("The ") + pl.col("title"))
        .otherwise(pl.col("title"))
        .alias("title")
    )
    return df


def mergeTranslations(df: pl.DataFrame) -> pl.DataFrame:
    for spanish, english in TRANSLATIONS.items():
        # Map entries to each english tranlation (could be many movies with the same english name)
        df = df.with_columns(
            (pl.col("title") == english).cast(pl.Int32)
            .cum_sum()
            .alias("english_title_group")
        )
        
        # Get the reviews & rating corresponding to each translation
        reviews_by_group = (
            df.filter((pl.col("title") == spanish).or_(pl.col("title") == english))
              .group_by("english_title_group")
              .agg(pl.concat_list("reviews"))
        )
        ratings_by_group = (
            df.filter(
                ((pl.col("title") == spanish).or_(pl.col("title") == english))
               )
              .group_by("english_title_group")
              .agg(pl.col("average_rating").mean())
        )
        
        # Join reviews
        df = df.join(
            reviews_by_group,
            on="english_title_group",
            how="left",
            suffix="_new"
        )
        
        # Join ratings
        df = df.join(
            ratings_by_group,
            on="english_title_group",
            how="left",
            suffix="_new"
        )
        
        # Update columns
        df = df.with_columns(
            # update reviews
            pl.when(pl.col("title") == english)
            .then(pl.col("reviews_new"))
            .otherwise(pl.col("reviews")),
            
            # update rating
            pl.when(pl.col("title") == english)
            .then(pl.col("average_rating_new"))
            .otherwise(pl.col("average_rating"))
        )
        df = df.drop(["reviews_new", "average_rating_new"])
      
    df = df.drop("english_title_group")  # drop groups column
    df = df.filter(~(pl.col("title").is_in(TRANSLATIONS.keys())))   # drop spanish titles
    return df


def modifySeriesDuration(
    df_series: pl.DataFrame, 
    df_episodes: pl.DataFrame
) -> pl.DataFrame:
    series_id_duration = (
        df_episodes
        .group_by("series_id")
        .agg(pl.col("duration_minutes").sum())
    )
    
    df_series = df_series.update(
        series_id_duration, 
        left_on="id", 
        right_on="series_id",
        maintain_order="left",
        how="inner"
    )
    
    return df_series


def cleanData(
    df_movies: pl.DataFrame,
    df_series: pl.DataFrame,
    df_episodes: pl.DataFrame
) -> tuple[pl.DataFrame, pl.DataFrame, pl.DataFrame]:    
    # 1) Remove trailing and leading blankspaces
    df_movies.with_columns(pl.col("title").str.strip_chars(' ').alias("title"))
    df_series.with_columns(pl.col("title").str.strip_chars(' ').alias("title"))
    df_episodes.with_columns(pl.col("title").str.strip_chars(' ').alias("title"))
    
    # 2) Deal with the "The"
    df_movies = theDealer(df_movies)
    df_series = theDealer(df_series)
    df_episodes = theDealer(df_episodes)
    
    # 3) Merge titles in Spanish & English
    df_movies = mergeTranslations(df_movies)
    df_series = mergeTranslations(df_series)
    df_episodes = mergeTranslations(df_episodes)
    
    # 4) Standarize length in minutes
        # movies
    df_movies = df_movies.with_columns(
        pl.when(pl.col("duration_minutes") > 245)
        .then(pl.col("duration_minutes")//60)
        .otherwise(pl.col("duration_minutes"))
    )
    
        # episodes
    df_episodes = df_episodes.with_columns(
        pl.when(pl.col("duration_minutes") > 119)
        .then(pl.col("duration_minutes")//60)
        .otherwise(pl.col("duration_minutes"))
    )
    
        # series
    df_series = modifySeriesDuration(df_series, df_episodes)
    
    # Return Dataframes
    return df_movies, df_series, df_episodes


def transformGenres(df: pl.DataFrame) -> pl.DataFrame:
    df_genres = (
        df
        .explode("genres")
        .with_columns(
            pl.col("genres").map_elements(
                lambda g: GENRE_TRANSFORMATIONS.get(g, [g]),
                return_dtype=pl.List(pl.String)
            ).alias("genres")
        )
        .explode("genres")
        .group_by("id", maintain_order=True)
        .agg(pl.col("genres").unique())
    )
    df = df.update(df_genres, on="id")
    return df


def addEpisodesToSeries(
    df_series: pl.DataFrame, 
    df_episodes: pl.DataFrame,
) -> pl.DataFrame:
    episodes_by_series_id = df_episodes.group_by("series_id").agg(pl.col("title"))
    episodes_by_series_id = episodes_by_series_id.rename({"title":"episodes"})
    df_series = df_series.join(
        episodes_by_series_id,
        left_on="id",
        right_on="series_id" 
    )
    return df_series


def countGenreByCategory(
    df_movies: pl.DataFrame,
    df_series: pl.DataFrame
) -> dict:
    # Count genres in movies 
    genre_movies = {}
    df_movie_genres = df_movies["genres"].explode()
    for g in df_movie_genres:
        if g in genre_movies:
            genre_movies[g] += 1
        else:
            genre_movies[g] = 1
            
    # Count genres in series 
    genre_series = {}
    df_series_genres = df_series["genres"].explode()
    for g in df_series_genres:
        if g in genre_series:
            genre_series[g] += 1
        else:
            genre_series[g] = 1
            
    return {
        "movies": genre_movies,
        "series": genre_series
    }


def plTransform(
    movies: dict, series: dict, episodes: dict
) -> tuple[pl.DataFrame, pl.DataFrame, pl.DataFrame, dict]:
    t1 = time()
    
    # Convert dictionaries into dataframes
    df_movies = pl.DataFrame(movies)
    df_series = pl.DataFrame(series)
    df_episodes = pl.DataFrame(episodes)
    
    # I) Clean Data
    df_movies, df_series, df_episodes = cleanData(df_movies, df_series, df_episodes)
    
    # II) Remove Non-Fiction Genres
    for g in NON_FICTION_GENRES:
        df_movies = df_movies.filter(~(pl.col("genres").list.contains(g)))
        df_series = df_series.filter(~(pl.col("genres").list.contains(g)))
        df_episodes = df_episodes.filter(~(pl.col("genres").list.contains(g)))
        
    # III) Remove, Combine & Split Genres
    df_movies = transformGenres(df_movies)
    df_series = transformGenres(df_series)
    df_episodes = transformGenres(df_episodes)
    
    # IV) Add episodes to series
    df_series = addEpisodesToSeries(df_series, df_episodes)
    
    # V) Count Movies, Series and Episodes in each genre
    genre_count = countGenreByCategory(df_movies, df_series)
    
    t2 = time()
    
    genre_count["polars_time"] = t2-t1
    
    return df_movies, df_series, df_episodes, genre_count


if __name__ == "__main__":
    movies, series, episodes = main_extract()
    df_movies, df_series, df_episodes, genre_count = plTransform(movies, series, episodes)
    print(genre_count)