import os
import sys
import random
from typing import List
import json

from locust import HttpUser, task, between, events

from examples.fake_generator import generate_fake_title

# Variables that are going to be modified from the data of files
SERIES_DICT: dict[str, List[str]] = {}
MOVIE_NAMES: List[str] = []

# Variables that are easier to CMD+P and CMD+V than to put in files
GENRE_NAMES = [
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
# Genre names that are going to be added by the functions below
NEW_GENRE_NAMES = [
    "French",
    "German",
    "Chineses",
    "Milanese",
    "Mexican",
    "Colombian",
    "Parisien",
    "Gambian",
    "Canadian",
    "Quebequois",
    "Ecuatorian",
    "Regian",
    "Roman",
    "Papal",
    "Insurrectionist",
    "Statist",
    "Bolchevik",
    "Menchevik"
]


@events.init.add_listener
def _(environment, **kwargs):
    """Configure Global Variables the way Locust asks (with the decorator I mean)"""
    global MOVIE_NAMES, SERIES_DICT
    
    movie_names_path='names/movie_names.txt'
    if os.path.exists(movie_names_path):
        with open(movie_names_path, 'r') as f:
            MOVIE_NAMES = [line.strip() for line in f if line.strip()]
            
    series_names_path='names/series.json'
    if os.path.exists(series_names_path):
        with open(series_names_path, 'r') as f:
            SERIES_DICT = json.load(f)
        

class WebsiteUser(HttpUser):
    """A class to run the test functions. 
    I tried to configure the task frecuencies the closer to real frecuencies
    """
    wait_time = between(1, 2.5)
    gnr_i = 0   # index to point to not run out of new genres to add
    
    # ADD CONTENT
    @task(5)    # These are the tasks frecuencies
    def add_movie(self):
            # Use set to store genres only once, then convert to list
        gnr_set = {random.choice(GENRE_NAMES) for _ in range(random.randint(1, 5))}
        payload = {
            "name": generate_fake_title(),
            "duration": random.randint(60, 400),
            "genres": list(gnr_set)
        }
        self.client.post(f"/movies", json=payload)
    
    @task(5) 
    def add_series(self):
        gnr_set = {random.choice(GENRE_NAMES) for _ in range(random.randint(1, 5))}
        payload = {
            "name": generate_fake_title(),
            "genres": list(gnr_set)
        }
        self.client.post(f"/series", json=payload)
    
    @task(4)   
    def add_episode(self):
        gnr_set = {random.choice(GENRE_NAMES) for _ in range(random.randint(1, 5))}
        series = random.choice(list(SERIES_DICT.keys()))
        payload = {
            "name": generate_fake_title(),
            "duration": random.randint(6, 150),
            "genres": list(gnr_set)
        }
        self.client.post(f"/series/{series}/episodes", json=payload)
    
    @task(1)
    def add_genre(self):
        if self.gnr_i >= len(NEW_GENRE_NAMES):
            return
        gnr_name = NEW_GENRE_NAMES[self.gnr_i]
        self.gnr_i += 1
        self.client.post(f"/genres", json={"name": gnr_name})
        
        
    # SELECT CONTENT
    @task(5)
    def select_all_content(self):
        size = random.randint(5, 100)
        page = random.randint(1, 7000//size)
        self.client.get(f"/content?page={page}&size={size}")
        
    @task(10)
    def select_all_movies(self):
        size = random.randint(5, 100)
        page = random.randint(1, 5000//size)
        self.client.get(f"/movies?page={page}&size={size}")
        
    @task(10)
    def select_all_series(self):
        size = random.randint(5, 100)
        page = random.randint(1, 2000//size)
        self.client.get(f"/series?page={page}&size={size}")
        
    @task(50)
    def select_movie(self):
        name = random.choice(MOVIE_NAMES)
        self.client.get(f"/movies/{name}")
        
    @task(50)
    def select_series(self):
        name = random.choice(list(SERIES_DICT.keys()))
        self.client.get(f"/series/{name}")
        
    @task(40)
    def select_episodes(self):
        kv_pair = random.choice(list(SERIES_DICT.items()))
        self.client.get(f"/series/{kv_pair[0]}/episodes/{random.choice(kv_pair[1])}")
        
    @task(20)
    def select_genre(self):
        name = random.choice(GENRE_NAMES)
        self.client.get(f"/genres/{name}")
    
    
    # RATE METHODS
    @task(20)
    def rate_movie(self):
        name = random.choice(MOVIE_NAMES)
        self.client.post(
            f"/movies/{name}/rate",
            json={"score":random.randint(1, 5)}
        )
    
    @task(20)  
    def rate_series(self):
        name = random.choice(list(SERIES_DICT.keys()))
        self.client.post(
            f"/series/{name}/rate",
            json={"score": random.randint(1, 5)}
        )
    
    @task(10)
    def rate_episode(self):
        kv_pair = random.choice(list(SERIES_DICT.items()))
        self.client.get(
            f"/series/{kv_pair[0]}/episodes/{random.choice(kv_pair[1])}",
            json={"score": random.randint(1, 5)}
        )
        
    
    # UPDATE METHODS
    @task(5)
    def update_movie(self):
        name = random.choice(MOVIE_NAMES)
        self.client.patch(
            f"/movies/{name}",
            json={"duration": random.randint(60, 200)}
        )
    
    @task(5)
    def update_series(self):
        name = random.choice(list(SERIES_DICT.keys()))
        self.client.patch(
            f"/series/{name}",
            json={"name": name+"a"}
        )
    
    @task(5)
    def update_episode(self):
        kv_pair = random.choice(list(SERIES_DICT.items()))
        self.client.patch(
            f"/series/{kv_pair[0]}/episodes/{random.choice(kv_pair[1])}",
            json={"duration": random.randint(20, 70)}
        )
    
    @task(5) 
    def update_genre(self):
        name = random.choice(GENRE_NAMES)
        self.client.patch(f"/genres/{name}", json={"name": name+"a"})
        
    
    # DELETE METHODS
    @task(3)
    def delete_movie(self):
        name = random.choice(MOVIE_NAMES)
        self.client.delete(f"/movies/{name}")

    @task(3)
    def delete_series(self):
        name = random.choice(MOVIE_NAMES)
        self.client.delete(f"/series/{name}")
    
    @task(3)
    def delete_episode(self):
        kv_pair = random.choice(list(SERIES_DICT.items()))
        self.client.delete(f"/series/{kv_pair[0]}/episodes/{random.choice(kv_pair[1])}")
    
    @task(1)
    def delete_genre(self):
        name = random.choice(GENRE_NAMES)
        self.client.delete(f"/genres/{name}")