import os
import requests
import datetime as dt
from typing import List, Optional
from dotenv import load_dotenv

import pymongo
from pymongo import MongoClient, UpdateOne

BASE_URL = "http://127.0.0.1:8000"

# Load secrets
load_dotenv()
MONGO_CONN = os.environ.get("MONGO_DB_CONN")


def getLastRunTime() -> Optional[dt.datetime]:
    client = MongoClient(MONGO_CONN)
    streamstats_db = client.StreamStats
    results_coll = streamstats_db.Results
    last_result = results_coll.find_one(sort=[("run_at", pymongo.DESCENDING)])
    
    if last_result:
        return dt.datetime.fromisoformat(last_result["run_at"])
    else:
        return None


def extractMovies(movies_dict: dict, last_updated: Optional[dt.datetime] = None):
    movies_url = "/movies"

    params = {
        "page": 1,
        "size": 50
    }
    response = requests.get(BASE_URL+movies_url, params=params)
    
    while response.status_code == 200:
        movies: List[dict] = response.json()
        
        for m in movies:
            if (not last_updated or last_updated 
                < dt.datetime.fromisoformat(m["last_updated_at"])):
                for key in movies_dict.keys():
                    movies_dict[key].append(m[key])
        
        params["page"] += 1
        response = requests.get(BASE_URL+movies_url, params=params)
    
    return movies_dict


def extractSeries(
    series_dict: dict, 
    episodes_dict: dict, 
    last_updated: Optional[dt.datetime] = None
):
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
            if (not last_updated or last_updated 
                < dt.datetime.fromisoformat(s["last_updated_at"])):
                for key in series_dict.keys():
                    series_dict[key].append(s[key])
            series_id = s["id"]
            series_episodes: List[dict] = requests.get(
                BASE_URL+episodes_url, 
                params={"ID": series_id}
            ).json()
            for ep in series_episodes:
                if (not last_updated or last_updated 
                    < dt.datetime.fromisoformat(ep["last_updated_at"])):
                    for key in episodes_dict.keys():
                        if key != "series_id":
                            episodes_dict[key].append(ep[key])
                    episodes_dict["series_id"].append(series_id)
        
        series_params["page"] += 1
        response = requests.get(BASE_URL+series_url, params=series_params)
                
    return series_dict, episodes_dict
                

def main_extract():
    # Dictionaries to store information about each category
    movies = {
        "id": [],
        "title": [],
        "duration_minutes": [],
        "genres": [],
        "average_rating": [],
        "reviews": [],
        "last_updated_at": [],
    }
    
    series = {
        "id": [],
        "title": [],
        "duration_minutes": [],
        "genres": [],
        "average_rating": [],
        "reviews": [],
        "number_of_episodes": [],
        "last_updated_at": [],
    }
    
    episodes = {
        "id": [],
        "series_id": [],
        "title": [],
        "season": [],
        "duration_minutes": [],
        "genres": [],
        "average_rating": [],
        "reviews": [],
        "last_updated_at": []
    }
    
    # Get last update time
    last_run_time = getLastRunTime()
    
    # Extract movies and series from the API
    movies = extractMovies(movies, last_run_time)
    series, episodes = extractSeries(series, episodes, last_run_time)
    
    return movies, series, episodes
    
    
if __name__ == "__main__":
    movies, series, episodes = main_extract()
    print(movies["title"][0:4])
    print(movies["last_updated_at"][0:4])