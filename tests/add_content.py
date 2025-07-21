# This file provides funcitons to add content

import requests

def add_movie():
    url = "http://127.0.0.1:8000/movies"
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
    url = "http://127.0.0.1:8000/series"
    payload = {
        'name': 'The Life and Times of Charlemagne',
        'genres': ['Historical']
    }
    
    response = requests.post(url, json=payload)
    
    print(response.status_code)
    print(response.json())
    return response.status_code
    
    
def add_episode():
    url = "http://127.0.0.1:8000/series/The Life and Times of Charlemagne/episodes"
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
    url = "http://127.0.0.1:8000/genres"
    payload = {
        'name': 'French',
    }
    
    response = requests.post(url, json=payload)
    
    print(response.status_code)
    print(response.json())
    return response.status_code

    
if __name__ == '__main__':
    #add_movie()
    #add_series()
    add_episode()   # Need to be executed after series
    #add_genre()