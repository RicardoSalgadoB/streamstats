import sys
import requests
from typing import List

BASE_URL = "http://127.0.0.1:8000"

def extractMovies(movies_dict: dict):
    movies_url = "/movies"

    params = {
        "page": 1,
        "size": 50
    }
    response = requests.get(BASE_URL+movies_url, params=params)
    
    while response.status_code == 200:
        movies: List[dict] = response.json()
        
        for m in movies:
            for key in movies_dict.keys():
                movies_dict[key].append(m[key])
        
        params["page"] += 1
        response = requests.get(BASE_URL+movies_url, params=params)
    
    return movies_dict


def extractSeries(series_dict: dict, episodes_dict: dict):
    series_url = "/series"
    episodes_url = "/series/episodes"
    
    series_params = {
        "page": 1,
        "size": 50
    }
    
    response = requests.get(BASE_URL+series_url, params=series_params)
    while response.status_code == 200:
        series: List[dict] = response.json()
        
        for s in series:
            for key in series_dict.keys():
                if key != "episodes":
                    series_dict[key].append(s[key])
            series_id = s["id"]
            series_episodes: List[dict] = requests.get(
                BASE_URL+episodes_url, 
                params={"ID": series_id}
            ).json()
            for ep in series_episodes:
                for key in episodes_dict.keys():
                    if key != "series_id":
                        episodes_dict[key].append(ep[key])
                ep["series_id"] = series_id
        
        series_params["page"] += 1
        response = requests.get(BASE_URL+series_url, params=series_params)
                
    return series_dict
                

def main_extract():
    # Dictionaries to store information about each category
    movies = {
        "id": [],
        "title": [],
        "duration_minutes": [],
        "genres": [],
        "average_rating": [],
        "reviews": []
    }
    
    series = {
        "id": [],
        "title": [],
        "duration_minutes": [],
        "genres": [],
        "average_rating": [],
        "reviews": [],
        "number_of_episodes": []
    }
    
    episodes = {
        "id": [],
        "series_id": [],
        "title": [],
        "season": [],
        "duration_minutes": [],
        "genres": [],
        "average_rating": [],
        "reviews": []
    }
    
    # Extract movies and series from the API
    movies = extractMovies(movies)
    series = extractSeries(series, episodes)
    
    return movies, series, episodes
    
    
if __name__ == "__main__":
    main_extract()
