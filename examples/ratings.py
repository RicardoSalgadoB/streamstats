import requests


def movie_example():
    url = "http://127.0.0.1:8000/rate/movie"
    payload = {
        "name": "Rouge One",
        "rating": 3
    }
    
    response = requests.post(url, json=payload)
    
    print(response.status_code)
    print(response.json())
    
    
def series_example():
    url = "http://127.0.0.1:8000/rate/series"
    payload = {
        "name": "The Bad Batch",
        "rating": 2
    }
    
    response = requests.post(url, json=payload)
    
    print(response.status_code)
    print(response.json())
    
    
def episode_example():
    url = "http://127.0.0.1:8000/series/&%7C/episodes/Kassa/rate"
    payload = {
        "score": 4
    }
    
    response = requests.post(url, json=payload)
    
    print(response.status_code)
    print(response.json())
    
    
if __name__ == "__main__":
    episode_example()