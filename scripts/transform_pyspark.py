import os
from typing import List
from time import time

import pandas as pd
import pyspark as ps
from pyspark.sql import SparkSession, DataFrame, Window
import pyspark.sql.functions as F
from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    ArrayType,
    IntegerType,
)

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


def theManagement(df: DataFrame) -> DataFrame:
    # Create set of titles
    titles_set = df.select("title").distinct()
    
    # Join where there exist a title with the "The "
    df = df.join(
        F.broadcast(titles_set.select(F.col("title").alias("the_title"))),
        on=F.col("the_title") == F.concat(F.lit("The "), F.col("title")),
        how="left"
    ).withColumn(
        "title",
        F.when(
            F.col("the_title").isNotNull(),
            F.concat(F.lit("The "), F.col("title"))
        ).otherwise(F.col("title"))
    ).drop("the_title")
    
    return df


def mergeTranslations(df: DataFrame) -> DataFrame:
    # Save the original columns of the dataframe
    original_cols = df.columns
    
    # Get all tranlations in english and spanish
    spanish_titles = list(TRANSLATIONS.keys())
    english_titles = []
    for english in TRANSLATIONS.values():
        english_titles.append(english)
        
    # Create mapping column
    title_mapping = F.col("title")
    for spanish, english in TRANSLATIONS.items():
        title_mapping = F.when(F.col("title") == spanish, english).otherwise(title_mapping)
    
    df_mapped = df.withColumn("english_group", title_mapping)  
    
    # Aggregation for reviews & ratins
    translation_data = df_mapped.filter(
        F.col("title").isin(spanish_titles + english_titles)
    ).groupBy("english_group").agg(
        F.flatten(F.collect_list("reviews")).alias("new_reviews"),
        F.avg("average_rating").alias("new_average_rating")
    )
    
    # Join reviews and ratings
    df_final = df_mapped.join(
        translation_data, 
        on="english_group", 
        how="left"
    ).withColumn(
        "reviews",
        F.when(F.col("new_reviews").isNotNull(), F.col("new_reviews"))
         .otherwise(F.col("reviews"))
    ).withColumn(
        "average_rating", 
        F.when(F.col("new_average_rating").isNotNull(), F.col("new_average_rating"))
         .otherwise(F.col("average_rating"))
    ).select(original_cols)
    
    return df_final


def modifySeriesDuration(
    df_series: DataFrame, 
    df_episodes: DataFrame
) -> DataFrame:
    series_id_duration = (
        df_episodes.groupBy("series_id").agg(F.sum("duration_minutes"))
    )
    
    series_cols = df_series.columns
    
    df_series = df_series.join(
        series_id_duration,
        on = F.col("series_id")==F.col("id"),
        how = "left"
    )
    
    df_series = df_series.withColumn(
        "duration_minutes",
        F.when(
            F.col("sum(duration_minutes)").isNotNull(),
            F.col("sum(duration_minutes)")
        ).otherwise(F.col("duration_minutes"))
    ).select(series_cols)
    
    return df_series


def cleanData(
    df_movies: DataFrame, 
    df_series: DataFrame, 
    df_episodes: DataFrame
):
    # 1) Remove trailing or leading blankspaces
    df_movies = df_movies.withColumn("title", F.trim("title"))
    df_series = df_series.withColumn("title", F.trim("title"))
    df_episodes = df_episodes.withColumn("title", F.trim("title"))
    
    # 2) Deal with "the"
    df_movies = theManagement(df_movies)
    df_series = theManagement(df_series)
    df_episodes = theManagement(df_episodes)
    
    # 3) Merge Titles in Spanish & English
    df_movies = mergeTranslations(df_movies)
    df_series = mergeTranslations(df_series)
    df_episodes = mergeTranslations(df_episodes)
    
    # 4) Standarize length in minutes
        # movies
    df_movies = df_movies.withColumn(
        "duration_minutes",
        F.when(
            F.col("duration_minutes") > 245,
            F.floor(F.col("duration_minutes") / F.lit(60))
        ).otherwise(F.col("duration_minutes"))
    )
    
        # episodes
    df_episodes = df_episodes.withColumn(
        "duration_minutes",
        F.when(
            F.col("duration_minutes") > 245,
            F.floor(F.col("duration_minutes") / F.lit(60))
        ).otherwise(F.col("duration_minutes"))
    )
    
        # series
    df_series = modifySeriesDuration(df_series, df_episodes)
    
    return df_movies, df_series, df_episodes


def transformGenres(df: DataFrame) -> DataFrame:
    original_cols = df.columns
    
    df_exploded = df.select(
        "id",
        F.explode("genres").alias("genres")
    )
    
    transform_genres_udf = F.udf(
        lambda g: GENRE_TRANSFORMATIONS.get(g, [g]), 
        ArrayType(StringType())
    )
    
    df_genres_exploded = df_exploded.withColumn(
        "genres",
        F.explode(transform_genres_udf(F.col("genres")))
    )
    
    df_genres = df_genres_exploded.groupBy("id").agg(F.collect_set("genres").alias("new_genres"))
    
    df = df.join(
        df_genres,
        on="id",
        how="left"
    )
    
    df = df.withColumn(
        "genres",
        F.when(
            F.col("new_genres").isNotNull(),
            F.col("new_genres")
        ).otherwise(F.col("genres"))
    ).select(original_cols)
    
    return df


def addEpisodesToSeries(
    df_series: DataFrame,
    df_episodes: DataFrame
) -> DataFrame:
    episodes_by_series_id = (
        df_episodes.groupBy("series_id").agg(F.collect_list("title"))
    )
    episodes_by_series_id = (
        episodes_by_series_id.withColumnRenamed(
            'collect_list("title")', 
            "episodes"
        )
    )
    df_series = df_series.join(
        episodes_by_series_id,
        on = F.col("series_id")==F.col("id"),
        how="inner"
    )
    return df_series


def countGenreByCategory(
    df_movies: DataFrame,
    df_series: DataFrame
) -> dict:
    # Count genres in movies 
    genre_movies = {}
    df_movie_genres = df_movies.select(
        F.explode("genres")
    ).rdd.flatMap(lambda x: x).collect()
    for g in df_movie_genres:
        if g in genre_movies:
            genre_movies[g] += 1
        else:
            genre_movies[g] = 1
            
    # Count genres in series 
    genre_series = {}
    df_series_genres = df_series.select(
        F.explode("genres")
    ).rdd.flatMap(lambda x: x).collect()
    for g in df_series_genres:
        if g in genre_series:
            genre_series[g] += 1
        else:
            genre_series[g] = 1
            
    return {
        "movies": genre_movies,
        "series": genre_series
    }
    

def psTransform(
    movies: dict, 
    series: dict, 
    episodes: dict
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, dict]:
    # Time PySpark execution
    t1 = time()
    
    # Initialize Spark Session
    spark = SparkSession.builder.getOrCreate()
    
    # A) Get DataFrames
    df_movies_pandas = pd.DataFrame(movies)
    movie_schema = StructType([
        StructField("id", IntegerType(), True),
        StructField("title", StringType(), True),
        StructField("duration_minutes", IntegerType(), True),
        StructField("genres", ArrayType(StringType()), True),
        StructField("average_rating", IntegerType(), True),
        StructField("reviews", ArrayType(StringType()), True),
    ])
    df_movies = spark.createDataFrame(df_movies_pandas, schema=movie_schema)
    df_series_pandas = pd.DataFrame(series)
    series_schema = StructType([
        StructField("id", IntegerType(), True),
        StructField("title", StringType(), True),
        StructField("duration_minutes", IntegerType(), True),
        StructField("genres", ArrayType(StringType()), True),
        StructField("average_rating", IntegerType(), True),
        StructField("reviews", ArrayType(StringType()), True),
        StructField("number_of_episodes", IntegerType(), True),
    ])
    df_series = spark.createDataFrame(df_series_pandas, schema=series_schema)
    df_episodes_pandas = pd.DataFrame(episodes)
    episodes_schema = StructType([
        StructField("id", IntegerType(), True),
        StructField("series_id", IntegerType(), True),
        StructField("title", StringType(), True),
        StructField("season", IntegerType(), True),
        StructField("duration_minutes", IntegerType(), True),
        StructField("genres", ArrayType(StringType()), True),
        StructField("average_rating", IntegerType(), True),
        StructField("reviews", ArrayType(StringType()), True),
    ])
    df_episodes = spark.createDataFrame(df_episodes_pandas, schema=episodes_schema)
    
    # B) Clean Data
    df_movies, df_series, df_episodes = cleanData(df_movies, df_series, df_episodes)
    
    # C) Remove Non-Fiction Genres
    for g in NON_FICTION_GENRES:
        df_movies = df_movies.filter(~(F.array_contains(F.col("genres"), g)))
        df_series = df_series.filter(~(F.array_contains(F.col("genres"), g)))
        df_episodes = df_episodes.filter(~(F.array_contains(F.col("genres"), g)))
    
    # D) Remove, Combine & Split Genres
    df_movies = transformGenres(df_movies)
    df_series = transformGenres(df_series)
    df_episodes = transformGenres(df_episodes)
    
    # E) Add episodes to series
    df_series = addEpisodesToSeries(df_series, df_episodes)
    
    # F) Count movies, series and episodes in each genre
    genre_count = countGenreByCategory(df_movies, df_series)
    
    t2 = time()
    
    genre_count["pyspark_time"] = t2-t1
    
    # Convert series to pandas to be returned
    df_movies_pandas = df_movies.toPandas()
    df_series_pandas = df_series.toPandas()
    df_episodes_pandas = df_episodes.toPandas()
    
    print(df_movies.show(5))
    print(df_series.show(5))
    print(df_episodes.show(5))
    print(genre_count)
    
    # Close session
    spark.stop()
    
    return (
        df_movies_pandas,
        df_series_pandas,
        df_episodes_pandas,
        genre_count
    )
    
if __name__  == "__main__":
    movies, series, episodes = main_extract()
    psTransform(movies, series, episodes)