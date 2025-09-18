# This file provides functions to update the contents added in add_content

import requests

def update_movie():
    url = "http://127.0.0.1:8000/movies/update?ID=1"
    payload = {
        'duration': 99
    }
    
    response = requests.patch(url, json=payload)
    
    print(response.status_code)
    print(response.json())
    return response.status_code
    
    
def update_series():
    url = "http://127.0.0.1:8000/series/update?ID=2"
    payload = {
        'name': 'The Life and Times of Charlesmagne'
    }
    
    response = requests.patch(url, json=payload)
    
    print(response.status_code)
    print(response.json())
    return response.status_code
    
    
def update_episode():
    url = "http://127.0.0.1:8000/episodes/update?ID=3&series_id=2"
    payload = {
        'season': 2
    }
    
    response = requests.patch(url, json=payload)
    
    print(response.status_code)
    print(response.json())
    return response.status_code
    
    
def update_genre():
    url = "http://127.0.0.1:8000/genres/update?ID=1"
    payload = {
        'name': 'Parisien'
    }
    
    response = requests.patch(url, json=payload)
    
    print(response.status_code)
    print(response.json())
    return response.status_code

    
if __name__ == '__main__':
    update_movie()
    update_series()
    update_episode()    # Execute after update series
    update_genre()