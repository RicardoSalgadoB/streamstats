import requests
import time
import schedule
import random

from generator.generators import ApiMovieGenerator, ApiSeriesGenerator

# Dictionary ensures consistency between score and reviews
reviews_by_score = {
    1: ["Shit", "Unwatchable", "Bordeline Terrorism", "Wilson would enjoy it"],
    2: ["A children's show", "Democrat propaganda", "Republican Propaganda"],
    3: ["Trivial", "Bland", "Sticks to the formula", "Lacks Innovation"],
    4: ["Good", "Only the acting fails", "A good cinema experience"],
    5: ["The genre at its finest", "Materpiece", "Just Gold", "Another era of filmaking"]
}


def add_new_movie(generator: ApiMovieGenerator):
    url = "http://host.docker.internal:8000/movies"
    payloads = generator.generate_content()
    
    for payload in payloads:
        response = requests.post(url, json=payload)
    
    
def add_new_series(generator: ApiSeriesGenerator):
    url_series = "http://host.docker.internal:8000/series"
    url_episodes = "http://host.docker.internal:8000/episodes?series_ID="
    series_payloads, eps_payloads = generator.generate_content()
    
    for payload in series_payloads:
        response = requests.post(url_series, json=payload)
        data = response.json()
        for ep_payload in eps_payloads:
            response = requests.post(
                url_episodes+str(data["id"]), 
                json=ep_payload
            )


def rate_content():
    _id = random.randint(1, 100000)
    url_rate = f"http://host.docker.internal:8000/content/rate?ID={_id}"
    score = random.randint(1, 5)
    review = random.choice(reviews_by_score[score])
    
    payload = {
        "score": score,
        "review": review,
    }
    
    response = requests.post(url_rate, json= payload)


def main():
    movie_gen = ApiMovieGenerator()
    series_gen = ApiSeriesGenerator()
    schedule.every(120).seconds.do(add_new_movie, movie_gen)
    schedule.every(120).seconds.do(add_new_series, series_gen)
    schedule.every(10).seconds.do(rate_content)
    
    while True:
        schedule.run_pending()
        time.sleep(1)
    
if __name__ == '__main__':
    main()