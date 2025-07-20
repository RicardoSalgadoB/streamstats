import os
import random

from locust import HttpUser, task, between, events


MOVIE_NAMES = []


@events.init.add_listener
def _(environment, **kwargs):
    global MOVIE_NAMES
    
    movie_names_path='names/movie_names.txt'
    if os.path.exists(movie_names_path):
        with open(movie_names_path, 'r') as f:
            MOVIE_NAMES = [line.strip() for line in f if line.strip()]
        

class WebsiteUser(HttpUser):
    wait_time = between(1, 10)
    
    @task(1)
    def get_all_movies(self):
        self.client.get(f"/movies")
        
    @task(10)
    def get_movie(self):
        movie_name = random.choice(MOVIE_NAMES)
        self.client.get(f"/movies/{movie_name}")
        
    @task(2)
    def rate_movie(self):
        movie_name = random.choice(MOVIE_NAMES)
        self.client.post(
            f"/movies/{movie_name}/rate",
            json={"score":random.randint(1, 5)}
        )
        