from time import time_ns

from app.utils import (
    find_movie,
    find_episode,
    find_series
)


def movie():
    t1 = time_ns()
    find_movie("The Cut of Deborah Roberts")
    t2 = time_ns()
    print(f"Finding The Cut of Deborah Roberts takes {(t2-t1)/1000:.0f} microseconds")
    
def series():
    t1 = time_ns()
    find_series("Large Test")
    t2 = time_ns()
    print(f"Finding Large Test takes {(t2-t1)/1000:.0f} microseconds")
    
def episode():
    t1 = time_ns()
    find_episode("Narkina 5", "&|")
    t2 = time_ns()
    print(f"Finding Narkina 5 takes {(t2-t1)/1000:.0f} microseconds")


if __name__ == "__main__":
    movie()