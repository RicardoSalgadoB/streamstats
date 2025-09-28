# This program rates some of the contents from Star Wars that were added previously.

import requests


def movie_example():
    url = "http://127.0.0.1:8000/movies/rate?name=Comedy Gold"
    payload = {
        "score": 4,
        "review": "Cool",
    }
    
    response = requests.post(url, json=payload)
    
    print(response.status_code)
    print(response.json())
    
    
def series_example():
    url = "http://127.0.0.1:8000/series/rate?name=The Funny Side of Early years teacher"
    payload = {
        "score": 2,
        "review": "A children's show"
    }
    
    response = requests.post(url, json=payload)
    
    print(response.status_code)
    print(response.json())
    
    
def episode_example():
    url = "http://127.0.0.1:8000/series/episodes/rate?series_ID=23&name=Cow Tales"
    payload = {
        "score": 4
    }
    
    response = requests.post(url, json=payload)
    
    print(response.status_code)
    print(response.json())
    
    
if __name__ == "__main__":
    #movie_example()
    #series_example()
    episode_example()