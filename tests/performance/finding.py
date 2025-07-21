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
    print(f"Finding The Cut of Deborah Roberts takes {(t2-t1):.3f} microseconds")
    
def series():
    t1 = time()
    find_series("Large Test")
    t2 = time()
    print(f"Finding Large Test takes {(t2-t1):.6f} microseconds")
    
def episode():
    t1 = time()
    find_episode("Narkina 5", "&|")
    t2 = time()
    print(f"Finding Narkina 5 takes {(t2-t1):.6f} microseconds")


if __name__ == "__main__":
    movie()