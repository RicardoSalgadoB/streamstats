import os
from typing import List

from dotenv import load_dotenv
from pymongo import MongoClient

from transform_pandas import pdTransform
from transform_polars import plTransform
from transform_pyspark import psTransform
from extract import main_extract

# Load secrets
load_dotenv()
MONGO_CONN = os.environ.get("MONGO_DB_CONN")

def combineFrameworks() -> tuple[List[dict], List[dict], List[dict], dict]:
    movies, series, episodes = main_extract()
    movies_pd, series_pd, episodes_pd, result_pd = pdTransform(movies, series, episodes)
    movies_pl, series_pl, episodes_pl, result_pl = plTransform(movies, series, episodes)
    movies_ps, series_ps, episodes_ps, result_ps = psTransform(movies, series, episodes)
    
    if (result_pd["pandas_time"] < result_pl["polars_time"]
        and result_pd["pandas_time"] < result_ps["pyspark_time"]):
        print("Pandas")
        result_pd["polars_time"] = result_pl["polars_time"]
        result_pd["pyspark_time"] = result_ps["pyspark_time"]
        return movies_pd, series_pd, episodes_pd, result_pd
    elif (result_pl["polars_time"] < result_pd["pandas_time"]
        and result_pl["polars_time"] < result_ps["pyspark_time"]):
        print("Polars")
        result_pl["pandas_time"] = result_pd["pandas_time"]
        result_pl["pyspark_time"] = result_ps["pyspark_time"]
        return movies_pl, series_pl, episodes_pl, result_pl
    else:
        print("PySpark")
        result_ps["pandas_time"] = result_pd["pandas_time"]
        result_ps["polars_time"] = result_pl["polars_time"]
        return movies_ps, series_ps, episodes_ps, result_ps

def main_load():
    # Get each collection
    client = MongoClient(MONGO_CONN)
    streamstats_db = client.StreamStats
    movies_coll = streamstats_db.Movies
    series_coll = streamstats_db.Series
    episodes_coll = streamstats_db.Episodes
    results_coll = streamstats_db.Results

    # Get the transformed data
    movies, series, episodes, result = combineFrameworks()
    
    # Load the data into Mongo
    movies_coll.insert_many(movies)
    series_coll.insert_many(series)
    episodes_coll.insert_many(episodes)
    results_coll.insert_one(result)
    
    
if __name__ == "__main__":
    main_load()