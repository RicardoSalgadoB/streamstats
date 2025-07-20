import requests


def movie_example():
    url = "http://127.0.0.1:8000/movies/Solo: A Star Wars Story/rate"
    payload = {
        "score": 3
    }
    
    response = requests.post(url, json=payload)
    
    print(response.status_code)
    print(response.json())
    
    
def series_example():
    url = "http://127.0.0.1:8000/series/The Bad Batch/rate"
    payload = {
        "score": 2
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
    movie_example()
    series_example()
    episode_example()