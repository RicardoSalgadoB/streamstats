import requests
from time import time

def select_movie():
    url = "http://127.0.0.1:8000/movies/A Sexy Tale"
    response = requests.get(url)
    
    print(response.status_code)
    print(response.json())
    return response.status_code
    
    
def select_series():
    url = "http://127.0.0.1:8000/series/The Life and Times of Charlesmagne"
    response = requests.get(url)
    
    print(response.status_code)
    print(response.json())
    return response.status_code
    
    
def select_episode():
    url = "http://127.0.0.1:8000/series/The Life and Times of Charlesmagne/episodes/"
    response = requests.get(url)
    
    print(response.status_code)
    print(response.json())
    return response.status_code
    
    
def select_genre():
    url = "http://127.0.0.1:8000/genres/French"
    response = requests.get(url)
    
    print(response.status_code)
    print(response.json())
    return response.status_code

    
if __name__ == '__main__':
    select_movie()
    #select_series()
    #select_episode()
    #select_genre()