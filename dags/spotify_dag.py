from datetime import datetime, timedelta
from textwrap import dedent

from airflow import DAG
from airflow.models import Variable
from airflow.operators.bash import BashOperator


def get_date(frmt: str="%Y%m%d") -> str:
    """
    Return yesterdays date in string format.
    """
    # Optional: set the timedelta value between 0-6
    # note that Spotify do not let you access older versions
    # of playlists. The backlog go as far back as 6 days.
    yesterday = datetime.now() - timedelta(1)
    return yesterday.strftime(frmt)

# Command line argument to be passed into BashOperators
params = { "date": get_date("%Y-%m-%d") }

default_args={
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=3),
}

with DAG(
    dag_id="el_spotify_featured_data",
    default_args=default_args,
    params=params,
    description="Extract featured tracks information by Spotify using their Web API",
    schedule="@daily",
    start_date=datetime(2023, 1, 1),
    catchup=False,
    tags=["spotify", "api", "google", "gcp", "data", "bigquery"],
) as dag:
    
    dag.doc_md = dedent(
    """ 
    ### Task Documentation
    ----
    Make calls to the Spotify Web API and extract track data 
    based on Spotify's recommended playlists. 

    #### The dag is defined in following steps.
    1. Extraction
        - Extract data from Spotify regions.
        - Load data into GCS bucket.
    2. Load
        - Load data into Bigquery.
        - Insert the data into a collective table.
    
    #### Command line arguments.
    **region** = Set which region  the extraction script should limit itself too. 
    
    Options.
    * AF = Africa
    * AS = Asia
    * EU = Europe
    * NASAOC = North America, South America and Ocenia
    
    **date** = Set which date the extraction should collect data from. 
    *Note Spotify only keeps a backlog of 6 days.*

    #### Formatting.
    The data is stored as a Parquet file, with a file convention
    of *ISO-YYYYMMDD.parquet* and within folder structure based
    on the *date*.

    The data is inserted to a *denormalized nested-repeated* table. 
    The table is *partitioned* by **date** and *clustered* by **region**
    first and country **ISO code** secondly.
    """
    )
     
    el_africa = BashOperator(
        task_id="el_africa",
        bash_command="python3 /opt/airflow/scripts/main.py AF {{params.date}}",
    )

    el_asia = BashOperator(
        task_id="el_asia",
        bash_command="python3 /opt/airflow/scripts/main.py AS {{params.date}}",
    )

    el_europe = BashOperator(
        task_id="el_europe",
        bash_command="python3 /opt/airflow/scripts/main.py EU {{params.date}}",
    )

    el_other = BashOperator(
        task_id="el_other",
        bash_command="python3 /opt/airflow/scripts/main.py NASAOC {{params.date}}",
    )

    load_to_bigquery = BashOperator(
        task_id="load_to_bigquery",
        bash_command="python3 /opt/airflow/scripts/bigqueryload.py {{params.date}}",
    )
    
    insert_to_bigtable = BashOperator(
        task_id="insert_to_bigtable",
        bash_command="python3 /opt/airflow/scripts/bigqueryinsert.py {{params.date}}",
    )
    
    [el_africa, el_asia, el_europe, el_other] >> load_to_bigquery >> insert_to_bigtable 
