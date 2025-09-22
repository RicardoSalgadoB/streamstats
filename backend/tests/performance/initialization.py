import os
from time import time_ns

import sqlalchemy as sa
from dotenv import load_dotenv

# Import base and
from app.models import Base, content_index, gender_index

# Load secret stuff
load_dotenv()
db_url = os.getenv("DB_URL")

# Create engine
ENGINE = sa.create_engine(db_url)


if __name__ == "__main__":
    # Tests how fast the tables and indexes can be created. Without alembic.
    Base.metadata.drop_all(ENGINE)
    t1 = time_ns()
    Base.metadata.create_all(ENGINE)
    t2 = time_ns()
    content_index.drop(bind=ENGINE)
    gender_index.drop(bind=ENGINE)
    t3 = time_ns()
    content_index.create(bind=ENGINE)
    gender_index.create(bind=ENGINE)
    t4 = time_ns()
    print(f"Creating all the tables and indexes takes {((t2-t1)+(t4-t3))/1000:.0f} microseconds")