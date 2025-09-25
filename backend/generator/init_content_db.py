# FILE TO POPULATE THE CATALOG WITH FAKE INITIAL CONTENT

# Standard Libraries
import os
import random
from typing import List
import json

# Pip Libraries
from dotenv import load_dotenv
from faker import Faker
import sqlalchemy as sa
import sqlalchemy.orm as orm

# My modules
from app.models import Movie, Episode, Series, Genre
from generator.generators import MovieGenerator, SeriesGenerator

# Load secrets
load_dotenv()
db_url = os.getenv("DB_URL")

# Create a sqlalchemy engine
ENGINE = sa.create_engine(db_url)
        

def generate_genres() -> List[Genre]:
    """Generate the all the genres of the catalog."""
    genre_names = {
            "Action", "Martial Arts", "Spy", "Military", "Superhero", "Disaster",
                "Chase", "Revenge", "Monster",
            "Adventure", "Jungle", "Desert", "Ocean", "Mountain", "Snow", 
                "Treasure Hunt", "Pirate", "Survival",
            "Animation", "Traditional 2D", "CGI", "3D", "Stop Motion",
                "Mixed Media", "Puppetry", "Rotoscoping",
            "Comedy", "Romanctic Comedy", "Slapstick", "Dark Comedy", "Screwball",
                "Parody", "Satire",
            "Crime", "Detective", "Film Noir", "Gangster", "Heist", "Hood Film",
                "Mystery", "Vigilante", "Police Procedural", "Organized Crime",
            "Drama", "Family Drama", "Psychological Drama", "Social Drama",
                "Political Drama", "Criminal Drama", "Legal Drama", "Medical Drama",
            "Fantasy", "High Fantasy", "Urban Fantasy", "Dark Fantasy",
                "Contemporary Fantasy", "Epic Fantasy", "Sword and Sorcery",
            "Horror", "Slasher", "Supernatural", "Psychological Horror", "Zombie",
                "Vampire", "Werewolf", "Ghost",
            "Musical", "Broadway", "Jukebox Musical", "Rock Opera", "Dance Musical",
                "Biographical Musical",
            "Romance",  "Romantic Comedy", "Historical Romance", 
                "Contemporary Romance", "Paranormal Romance", "Erotic Romance",
            "Science_Fiction", "Space Opera", "Science Fantasy", "Cyberpunk",
                "Dystopian", "Time Travel", "Alien Contact", "Post-Apocalyptic",
            "Sci-Fi",
            "Thriller", "Psychological Thriller", "Political Thriller",
                "Techno Thriller", "Medical Thriller", "Legal Thriller",
                "Conspiracy Thriller",
            "Western", "Spaghetti Western", "Revisionist Western", "Comedy Western",
                "Acid Western", "Space Western", "Contemporary Western",
            "Sports", "Foorball", "Basketball", "Baseball", "Boxing", "Racing",
                "Olympics",
            "Documentary", "Historical", "Nature", "Political", "Social Issues",
                "Biography", "True Crime", "Science", "Sports",
            "Reality", "Competition", "Dating", "Lifestyle", "Family",
                "Makeover", "Travel"
    }
    genre_objs = []
    
    # Create each genre object
    for name in list(genre_names):
        genre_objs.append(Genre(name=name))
        
    return genre_objs


def generate_movies(genres: List[Genre] ,num: int = 5000) -> List[Movie]:
    """Generates `num` fake movies of the catalog."""
    # List to store movies
    movies = []
    
    # Create object to generate movies
    for i in range(num):
        if i%(num//10) == 0:
            print(f'{i}/{num} movies generated')
        movie_generator = MovieGenerator()
        translations = movie_generator.generate_content(genres)
        for m in translations:
            movies.append(m)
    return movies   # return the list of movies


def generate_series(genres: List[Genre], num: int = 2000):
    """Generates `num` fake series (with episodes) for the catalog. Episodes included"""
    series = []
   
    # Instantiate object to generate series
    for i in range(num):
        if i%(num//10) == 0:
            print(f'{i}/{num} series generated')
        series_generator = SeriesGenerator()
        translations = series_generator.generate_content(genres) # Generate a series
        for s in translations:
            series.append(s)
    return series # return list of series

                
if __name__ == '__main__':
    # Generate genres, movies and series
    print("Generating genres...")
    genres = generate_genres()
    print("Generating movies...")
    movies = generate_movies(genres, 200)
    print("Generating series...")
    series = generate_series(genres, 100)
    
    # Commit the objects to the database
    print("Adding content to the database...")
    with orm.Session(ENGINE) as session:
        for g in genres:
            session.add(g)
        for m in movies:
            session.add(m)
        for s in series:
            session.add(s)
        session.commit()
        
    print("Generation is done")
