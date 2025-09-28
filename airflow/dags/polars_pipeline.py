import datetime as dt
from airflow.decorators import dag, task
import sys
sys.path.append('/opt/airflow')

from scripts.extract import main_extract
from scripts.transform_pandas import pdTransform
from scripts.transform_polars import plTransform
from scripts.transform_pyspark import psTransform
from scripts.load_mongodb import main_load, combineFrameworks

# DAG configuration
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': dt.datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': dt.timedelta(minutes=5),
}

@dag(
    dag_id='streamstats_pipeline_polars',
    default_args=default_args,
    description='ETL pipeline for movie data using multiple frameworks',
    schedule='@daily',
    catchup=False,
    tags=['etl', 'streamstats', 'mongodb'],
)
def movie_etl_pipeline():
    """
    Main DAG function that defines the movie ETL pipeline.
    Processes movie, series, and episodes data using pandas, polars, and pyspark.
    """
    
    @task(task_id='extract_data')
    def extract():
        """
        Extract raw data from source systems.
        Returns: Tuple of (movies, series, episodes) data
        """
        movies, series, episodes = main_extract()
        return {
            'movies': movies,
            'series': series,
            'episodes': episodes
        }
    
    @task(task_id='transform_with_polars')
    def transform_polars(data_dict):
        """
        Transform data using polars framework.
        Args: data_dict - Dictionary containing movies, series, episodes data
        Returns: Transformed data using polars
        """
        movies = data_dict['movies']
        series = data_dict['series']
        episodes = data_dict['episodes']
        
        movies_pl, series_pl, episodes_pl, result_pl = plTransform(movies, series, episodes)
        return {
            'movies_pl': movies_pl,
            'series_pl': series_pl,
            'episodes_pl': episodes_pl,
            'result_pl': result_pl
        }
    
    @task(task_id='load_to_mongodb')
    def load_mongo(data):
        """
        Combine data from all frameworks and load to MongoDB.
        Args: 
            pandas_data - Transformed data from pandas
            polars_data - Transformed data from polars  
            pyspark_data - Transformed data from pyspark
        """
        # Extract all categories
        movies = data['movies_pl']
        series = data['series_pl']
        episodes = data['episodes_pl']
        results = data['result_pl']
        
        # Load combined data to MongoDB
        main_load(movies, series, episodes, results)
        return "Data successfully loaded to MongoDB"
    
    # Define task dependencies
    extracted_data = extract()
    
    # Transform data with polars
    polars_transformed = transform_polars(extracted_data)
    
    # Load combined data to MongoDB
    load_result = load_mongo(polars_transformed)

# Instantiate the DAG
movie_etl_dag = movie_etl_pipeline()
    
