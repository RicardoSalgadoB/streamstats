from time import time_ns

from app.utils import (
    show_all,
    show_movies,
    show_series,
    show_eps_of_series,
    show_genres
)


def all():
    t1 = time_ns()
    show_all()
    t2 = time_ns()
    print(f"Showing all content takes {(t2-t1)/1000:.0f} microseconds")

def movies():
    t1 = time_ns()
    print(show_movies())
    t2 = time_ns()
    print(f"Showing all movies takes {(t2-t1)/1000:.0f} microseconds")

def series():
    t1 = time_ns()
    show_series()
    t2 = time_ns()
    print(f"Showing all series takes {(t2-t1)/1000:.0f} microseconds")
    
def episodes():
    t1 = time_ns()
    show_eps_of_series("&|")
    t2 = time_ns()
    print(f"Showing all episodes of Andor takes {(t2-t1)/1000:.0f} microseconds")

def genres():
    t1 = time_ns()
    show_genres()
    t2 = time_ns()
    print(f"Showing all genres takes {(t2-t1)/1000:.0f} microseconds")


if __name__ == "__main__":
    # Tests how fast paginated information can be shown. Beware teh cache.
    t1 = time_ns()
    all()
    #movies()   # already shown in all
    #series()
    episodes()
    genres()
    t2 = time_ns()
    print(f"Showing all the series, movies, episodes and genres takes {(t2-t1)/1000:.0f} microseconds")