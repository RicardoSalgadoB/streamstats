import requests

def update_movie():
    url = "http://127.0.0.1:8000/movies/The Life and Times of Alexander the Great"
    payload = {
        'duration': 99
    }
    
    response = requests.patch(url, json=payload)
    
    print(response.status_code)
    print(response.json())
    return response.status_code
    
    
def update_series():
    url = "http://127.0.0.1:8000/series/The Life and Times of Charlemagne"
    payload = {
        'name': 'The Life and Times of Charlesmagne'
    }
    
    response = requests.patch(url, json=payload)
    
    print(response.status_code)
    print(response.json())
    return response.status_code
    
    
def update_episode():
    url = "http://127.0.0.1:8000/series/The Life and Times of Charlesmagne/episodes/Bad Brother and a Worse Border"
    payload = {
        'season': 2
    }
    
    response = requests.patch(url, json=payload)
    
    print(response.status_code)
    print(response.json())
    return response.status_code
    
    
def update_genre():
    url = "http://127.0.0.1:8000/genres/French"
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
    update_episode()
    update_genre()