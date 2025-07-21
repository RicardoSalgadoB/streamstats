from examples.star_wars import Star_Wars
import sqlalchemy as sa
import sqlalchemy.orm as orm
from time import time_ns


if __name__ == "__main__":
    # tests how fast the star wars catalog is added
    t1 = time_ns()
    Star_Wars()
    t2 = time_ns()
    
    print(f"Adding (some of) the contents of Star Wars takes {(t2-t1)/1000:.0f} microseconds")