# This file provides functions to delete teh content added and update in add_content and update_content

import requests

def delete_movie():
    url = "http://127.0.0.1:8000/movies/remove?ID=1"
    response = requests.delete(url)
    
    print(response.status_code)
    print(response.json())
    return response.status_code
    
    
def delete_series():
    url = "http://127.0.0.1:8000/series/remove?ID=2"
    response = requests.delete(url)
    
    print(response.status_code)
    print(response.json())
    return response.status_code 
    
    
def delete_episode():
    url = "http://127.0.0.1:8000/episodes/remove?ID=3"
    response = requests.delete(url)
    
    print(response.status_code)
    print(response.json())
    return response.status_code
    
    
def delete_genre():
    url = "http://127.0.0.1:8000/genres/remove?ID=1"
    response = requests.delete(url)
    
    print(response.status_code)
    print(response.json())
    return response.status_code

    
if __name__ == '__main__':
    delete_movie()
    delete_series()
    delete_episode()
    delete_genre()