# This file provides functions to delete teh content added and update in add_content and update_content

import requests

def delete_movie():
    url = "http://127.0.0.1:8000/movies/The Life and Times of Alexander the Great"
    response = requests.delete(url)
    
    print(response.status_code)
    print(response.json())
    return response.status_code
    
    
def delete_series():
    url = "http://127.0.0.1:8000/series/The Life and Times of Charlesmagne"
    response = requests.delete(url)
    
    print(response.status_code)
    print(response.json())
    return response.status_code 
    
    
def delete_episode():
    url = "http://127.0.0.1:8000/series/The Life and Times of Charlesmagne/episodes/Bad Brother and a Worse Border"
    response = requests.delete(url)
    
    print(response.status_code)
    print(response.json())
    return response.status_code
    
    
def delete_genre():
    url = "http://127.0.0.1:8000/genres/Parisien"
    response = requests.delete(url)
    
    print(response.status_code)
    print(response.json())
    return response.status_code

    
if __name__ == '__main__':
    delete_movie()
    delete_series()
    delete_episode()
    delete_genre()