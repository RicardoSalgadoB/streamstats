import os
from time import time_ns

import sqlalchemy as sa
from dotenv import load_dotenv

from app.tables import (
    Base,
    Genre,
    Content,
    Movie,
    Episode,
    Serie
)

load_dotenv()
db_url = os.getenv("DB_URL")
ENGINE = sa.create_engine(db_url)

if __name__ == "__main__":
    Base.metadata.drop_all(ENGINE)
    t1 = time_ns()
    Base.metadata.create_all(ENGINE)
    t2 = time_ns()
    
    print(f"Creating all the tables takes {(t2-t1)/1000:.0f} microseconds")