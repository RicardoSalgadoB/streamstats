import datetime as dt
from airflow.decorators import dag, task
import sys
sys.path.append('/opt/airflow')

from pyspark import SparkContext
from pyspark.sql import SparkSession
from airflow.providers.apache.spark.decorators import pyspark

from scripts.extract import main_extract
from scripts.transform_pandas import pdTransform
from scripts.transform_polars import plTransform
from scripts.transform_pyspark import psTransform
from scripts.load_mongodb import main_load, combineFrameworks

# DAG configuration
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': dt.datetime(2025, 9, 29, 2),
    'end_date': dt.datetime(2025, 9, 29, 5),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': dt.timedelta(minutes=5),
}

@dag(
    dag_id='streamstats_pipeline_pyspark',
    default_args=default_args,
    description='ETL pipeline for movie data using multiple frameworks',
    schedule='0 * * * *',
    catchup=False,
    tags=['etl', 'streamstats', 'mongodb', 'pyspark'],
)
def streamstats_pipeline():
    """
    Main DAG function that defines the streamstats ETL pipeline.
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
    
    @task.pyspark(task_id='transform_with_pyspark', conn_id="spark_conn")
    def transform_pyspark(data_dict, spark: SparkSession, sc: SparkContext):
        """
        Transform data using pyspark framework.
        Args: data_dict - Dictionary containing movies, series, episodes data
        Returns: Transformed data using pyspark
        """
        movies = data_dict['movies']
        series = data_dict['series']
        episodes = data_dict['episodes']
        
        movies_ps, series_ps, episodes_ps, result_ps = psTransform(movies, series, episodes)
        return {
            'movies_ps': movies_ps,
            'series_ps': series_ps,
            'episodes_ps': episodes_ps,
            'result_ps': result_ps
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
        movies = data['movies_ps']
        series = data['series_ps']
        episodes = data['episodes_ps']
        results = data['result_ps']
        
        # Load combined data to MongoDB
        main_load(movies, series, episodes, results)
        return "Data successfully loaded to MongoDB"
    
    # Define task dependencies
    extracted_data = extract()
    
    # Transform data with different frameworks (can run in parallel)
    pyspark_transformed = transform_pyspark(extracted_data)

    # Load combined data to MongoDB
    load_result = load_mongo(pyspark_transformed)

# Instantiate the DAG
movie_etl_dag = streamstats_pipeline()
    
