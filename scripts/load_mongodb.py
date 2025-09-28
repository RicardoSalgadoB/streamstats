import os
import datetime as dt
from typing import List

from dotenv import load_dotenv
from pymongo import MongoClient, UpdateOne

from transform_pandas import pdTransform
from transform_polars import plTransform
from transform_pyspark import psTransform
from extract import main_extract

# Load secrets
load_dotenv()
MONGO_CONN = os.environ.get("MONGO_DB_CONN")

def combineFrameworks(
    movies_pd, series_pd, episodes_pd, result_pd,
    movies_pl, series_pl, episodes_pl, result_pl,
    movies_ps, series_ps, episodes_ps, result_ps
) -> tuple[List[dict], List[dict], List[dict], dict]:
    if not result_pl and not result_ps:
        return movies_pd, series_pd, episodes_pd, result_pd
    elif not result_pd and not result_ps:
        return movies_pl, series_pl, episodes_pl, result_pl
    elif not result_pd and not result_pl:
        return movies_ps, series_ps, episodes_ps, result_ps
    
    
    if (result_pd["pandas_time"] < result_pl["polars_time"]
        and result_pd["pandas_time"] < result_ps["pyspark_time"]):
        print("Pandas")
        if result_pl:
            result_pd["polars_time"] = result_pl["polars_time"]
        if result_ps:
            result_pd["pyspark_time"] = result_ps["pyspark_time"]
        return movies_pd, series_pd, episodes_pd, result_pd
    
    elif (result_pl["polars_time"] < result_pd["pandas_time"]
        and result_pl["polars_time"] < result_ps["pyspark_time"]):
        print("Polars")
        if result_pd:
            result_pl["pandas_time"] = result_pd["pandas_time"]
        if result_ps:
            result_pl["pyspark_time"] = result_ps["pyspark_time"]
        return movies_pl, series_pl, episodes_pl, result_pl
    
    else:
        print("PySpark")
        if result_pd:
            result_ps["pandas_time"] = result_pd["pandas_time"]
        if result_pl:
            result_ps["polars_time"] = result_pl["polars_time"]
        return movies_ps, series_ps, episodes_ps, result_ps


def main_load(movies, series, episodes, result) -> None:
    # Get each collection
    client = MongoClient(MONGO_CONN)
    streamstats_db = client.StreamStats
    movies_coll = streamstats_db.Movies
    series_coll = streamstats_db.Series
    episodes_coll = streamstats_db.Episodes
    results_coll = streamstats_db.Results

    # Get the transformed data
    #movies, series, episodes, result = combineFrameworks()
    
    # Upsert the data into Mongo
        # List to store operations
    movies_operations = []
    series_operations = []
    episodes_operations = []
    
    # For each movie add an upsert operation with the given id
    for m in movies:
        filter_query = {"_id" : m["_id"]}
        update_op = {'$set' : m}
        movies_operations.append(
            UpdateOne(
                filter_query,
                update_op,
                upsert=True,
            )
        )
        
    # For each series create an upsert operation
    for s in series:
        filter_query = {"_id" : s["_id"]}
        update_op = {'$set' : s}
        series_operations.append(
            UpdateOne(
                filter_query,
                update_op,
                upsert=True,
            )
        )
    
    # For each episode create an upsert operation 
    for ep in episodes:
        filter_query = {"_id" : ep["_id"]}
        update_op = {'$set' : ep}
        episodes_operations.append(
            UpdateOne(
                filter_query,
                update_op,
                upsert=True,
            )
        )
    
    # Execute all save operations
    if movies_operations:
        movies_coll.bulk_write(movies_operations)
        
    if series_operations:
        series_coll.bulk_write(series_operations)
        
    if episodes_operations:
        episodes_coll.bulk_write(episodes_operations)
    
    # Add the a time entry to the result and save it
    result["run_at"] = dt.datetime.now(dt.UTC).isoformat()
    results_coll.insert_one(result)
    
    
if __name__ == "__main__":
    movies, series, episodes = main_extract()
    movies_pd, series_pd, episodes_pd, result_pd = pdTransform(movies, series, episodes)
    movies_pl, series_pl, episodes_pl, result_pl = plTransform(movies, series, episodes)
    movies_ps, series_ps, episodes_ps, result_ps = psTransform(movies, series, episodes)
    movies, series, episodes, results = combineFrameworks(
        movies_pd, series_pd, episodes_pd, result_pd,
        movies_pl, series_pl, episodes_pl, result_pl,
        movies_ps, series_ps, episodes_ps, result_ps
    )
    main_load(movies, series, episodes, results)