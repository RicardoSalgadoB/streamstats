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
    Serie,
    content_index
)

load_dotenv()
db_url = os.getenv("DB_URL")
ENGINE = sa.create_engine(db_url)


if __name__ == "__main__":
    Base.metadata.drop_all(ENGINE)
    t1 = time_ns()
    Base.metadata.create_all(ENGINE)
    t2 = time_ns()
    content_index.drop(bind=ENGINE)
    t3 = time_ns()
    content_index.create(bind=ENGINE)
    t4 = time_ns()
    print(f"Creating all the tables takes {((t2-t1)+(t4-t3))/1000:.0f} microseconds")