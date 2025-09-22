import requests
import time
import schedule

from generator.generators import ApiMovieGenerator, ApiSeriesGenerator

def add_new_movie(generator: ApiMovieGenerator):
    url = "http://127.0.0.1:8000/movies"
    payloads = generator.generate_content()
    
    for payload in payloads:
        response = requests.post(url, json=payload)
        print(response.status_code)
        print(response.json())
    
    
def add_new_series(generator: ApiSeriesGenerator):
    url_series = "http://127.0.0.1:8000/series"
    url_episodes = "http://127.0.0.1:8000/episodes?series_ID="
    series_payloads, eps_payloads = generator.generate_content()
    
    for payload in series_payloads:
        response = requests.post(url_series, json=payload)
        data = response.json()
        print(response.status_code)
        print(data)
        for ep_payload in eps_payloads:
            response = requests.post(
                url_episodes+str(data["id"]), 
                json=ep_payload
            )
            print(response.status_code)
            print(response.json())


def main():
    movie_gen = ApiMovieGenerator()
    series_gen = ApiSeriesGenerator()
    schedule.every(5).seconds.do(add_new_movie, movie_gen)
    schedule.every(5).seconds.do(add_new_series, series_gen)
    
    while True:
        schedule.run_pending()
        time.sleep(1)
    
if __name__ == '__main__':
    main()