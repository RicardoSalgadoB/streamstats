from time import time

from app.utils import (
    find_movie,
    find_episode,
    find_series
)


def movie():
    t1 = time()
    find_movie("A Sexy Tale")
    t2 = time()
    print(f"Finding A Sexy Tale takes {(t2-t1):.6f} seconds")
    
def series():
    t1 = time()
    find_series("Large Test")
    t2 = time()
    print(f"Finding Large Test takes {(t2-t1):.6f} seconds")
    
def episode():
    t1 = time()
    find_episode("Narkina 5", "&|")
    t2 = time()
    print(f"Finding Narkina 5 takes {(t2-t1):.6f} seconds")


if __name__ == "__main__":
    # Tests how fasts finds can be executed. Beware of the Cache
    movie()
    series()
    episode()