# This file provides funcitons to select the contents add and updated in add_content and update_content, respectiviely

import requests
from time import time

def select_movie():
    url = "http://127.0.0.1:8000/movies/find?ID=1"
    response = requests.get(url)
    
    print(response.status_code)
    print(response.json())
    return response.status_code
    
    
def select_series():
    url = "http://127.0.0.1:8000/series/find?ID=2"
    response = requests.get(url)
    
    print(response.status_code)
    print(response.json())
    return response.status_code
    
    
def select_episode():
    url = "http://127.0.0.1:8000/episodes/find?ID=3&series_id=2"
    response = requests.get(url)
    
    print(response.status_code)
    print(response.json())
    return response.status_code
    
    
def select_genre():
    url = "http://127.0.0.1:8000/genres/find?ID=1"
    response = requests.get(url)
    
    print(response.status_code)
    print(response.json())
    return response.status_code

    
if __name__ == '__main__':
    select_movie()
    select_series()
    select_episode()
    select_genre()