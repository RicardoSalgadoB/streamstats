import requests

def add_movie():
    url = "http://127.0.0.1:8000/movies/add"
    payload = {
        'name': 'The Life and Times of Alexander the Great',
        'duration': 98,
        'genres': ['Historical']
    }
    
    response = requests.post(url, json=payload)
    
    print(response.status_code)
    print(response.json())
    return response.status_code
    
    
def add_series():
    url = "http://127.0.0.1:8000/series/add"
    payload = {
        'name': 'The Life and Times of Charlemagne',
        'genres': ['Historical']
    }
    
    response = requests.post(url, json=payload)
    
    print(response.status_code)
    print(response.json())
    return response.status_code
    
    
def add_episode():
    url = "http://127.0.0.1:8000/series/The Life and Times of Charlemagne/episodes/add"
    payload = {
        'name': 'Bad Brother and a Worse Border',
        'duration': 56,
        'season': 1,
        'genres': ['Historical']
    }
    
    response = requests.post(url, json=payload)
    
    print(response.status_code)
    print(response.json())
    return response.status_code
    
    
def add_genre():
    url = "http://127.0.0.1:8000/genres/add"
    payload = {
        'name': 'French',
    }
    
    response = requests.post(url, json=payload)
    
    print(response.status_code)
    print(response.json())
    return response.status_code

    
if __name__ == '__main__':
    add_movie()
    add_series()
    add_episode()
    add_genre()