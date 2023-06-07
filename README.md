## On this page
* [Purpose](#purpose)
* [Scope](#scope)
* [Infrastructure](#infrastructure)
  * [The Data Stack](#the-data-stack)
  * [Extrack and Load](#extrack-and-load)
  * [Orchestration](#orchestration)
  * [Data Warehouse](#data-warehouse)
  * [Transformation](#transformation)
  * [Visuallization](#visuallization)
* [Python Guide](#python-guide)
  * [Prerequisites](#prerequisites)
  * [Variables](#variables)
  * [Tasks](#tasks)
* [The Result](#the-result)
  * [Spotify Playlists](#spotify-playlists)
* [Summary](#summary)
  * [Future Revisions](#future-revisions)

| NOTE: This is a Proof of Concept Documentation |
| :--- | 
| This project is meant for cloud development. It acts as a proof of concept for what can be done with the Spotify Web API. The configuration supports basic configuration using environment variables or an .env file. Feel free to modify this project to suit your needs. |

## Purpose
The goal of this project is to highlight the songs that Spotify recommend in their official playlists and what character said songs possess. The data will help upcoming artist understand the Spotify market audience and better target their efforts. This project also conceptually describes on high level the componenents which all together are defined as an ELT data pipeline.  

## Scope
The project is limited to a weeks worth of data (~30 million rows of data) for brevity. The DAG however should return ~1.5 billion rows of data annually. This document is limited to describe the pipeline conceptually, as there are other resources that describe it in more detail.

## Infrastructure
### The Data Stack
![Data stack made in Canva](https://github.com/blktheta/spotify-image/blob/1aa20965f2e2fd54cbc9b05d2f72e2b22e545cb7/images/data-stack.png "ELT data stack")

The project use Terraform to manage cloud resources. The data model is diagrammed in Lucid Chart and the dashboard in Looker Studio. The extraction, loading and transformation part of the stack is all overseen by Ariflow. 

| Stage | Tools |
| :--- | :---: |
| Infrastructure | Terraform |
| Diagramming | Lucid Chart & Canva |
| Extraction | Python Code |
| Loading | Python Code |
| Orchestration | Airflow & Docker |
| Data Warehouse | Google Cloud Storage |
| Transformations | Google Cloud BigQuery |
| Data Visualization | Google Cloud Looker |

### Extrack and Load
The project use custom made pipeline built in `Python 3.10` and orchestrated in `Airflow 2.5.3` run in a `Docker` container. This ELT pipeline requires the owner to be responsible for building, maintaining, or orchestrating the movement of data from the data source into the data warehouse.

The RAW data loaded into the data warehouse comes from the [Spotify Web API](https://developer.spotify.com/documentation/web-api). The data runs though an Airflow pipeline and is stored raw in Google Cloud Storage. The *Replication Frequency* (RF) is set to 24h and *Service Level Objective* (SLO) to 3 hours. The numbers may change if Spotify updates their rate limits in near future. 

### Orchestration
This pipeline use Airflow on a Docker container for orchestration. The specific setup can be found in the `docker-compose.yaml` file. It is based on the offical `docker-compose.yaml` file fetched from the Airflow documentation [here](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html). 

### Data Warehouse
The project use Google Cloud Storage as data warehouse. Its seamless integration with other GC features and the 90 days trial makes it a great contendor for smaller projects.

The project use two primary databases `raw` and `prep`, a third `prod` database could be used to further transform and model the data for business use. The `raw` database is where data is first loaded into Cloud Storage; the `prep` database is controlled by BigQuery and is for data that is ready for analysis. 

### Transformation
The project use Google Cloud BigQuery for all `prep` transformation. The data modeling follow a star schema, with a *denormalized* "fact" table, rather then *normalized* dimension tables. The star schema supports analytical queries better for it allows the use of running simpler queries because the limited number of joins. It also performs faster aggregations that improve the query performance.  

![Star schema made in Lucid Chart](https://github.com/blktheta/spotify-image/blob/248b34dee8a0417c64ca91800276bc251f42e272/images/star-schema.png "Denormalized star schema")

BigQuery natively supports *nested* and *repeated* structures in JSON or AVRO input data, records can therefore be expressed more naturally. For more information see the documentation at [Google](https://cloud.google.com/bigquery/docs/nested-repeated). For now the thing to remember is two fold:
1. BigQuery automatically flattens nested fields when querying.
2. BigQuery automatically groups data by "row" when querying one or more repeated fiels.

Continuing with the above schema the following key things are of note:

* A timestamp in `featured_track` can have multiple `playlists` and
* A playlist in `featured_track` can have multiple `tracks` and
* A track in `featured_track` belongs to a single `artist` and
* A track in `featured_track` belongs to a single `album` and
* A track in `featured_track` belongs to a single `audio-feature`.

Putting it all together we arrive at an alternative representation of the initial *denormalized* schema. A shrunked version, for presentation sake, of the above schema is represented as followed:

| feature | region | country | playlist.name | plalylist.track.name | playlist.track.artist.name | ... |
| --- | --- | --- | --- | --- | --- | --- |
| 2023-05-24 | Europe | Sweden | It's Hits Sweden | Tattoo | Loreen | ... |
|  |  |  |  | Under någon ny | Miriam Bryant | ... |
|  |  |  | Made in Sweden | Måndagsbarn | Olivia Lobato | ... |
|  |  |  |  | 5D | Lykke Li | ... |
|  |  |  |  | Superstar | Bianca Ingrosso | ... |
| 2023-05-24 | Asia | Korea | Dalkom Cafe | Mirror | Sunday Moon | ... |
|  |  |  |  | Sell My Heart | Junggigo | ... |
|  |  |  | Soundtracks | Photo of My Mind | Song Ga In | ... |

### Visuallization
The project use Google Cloud Looker Studio as a data visualization tool. A sample report is appended to the project to showcase the simple usage of the `prep` data. 

## Python Guide
The project is written exclusively in Python, except a SQL query, and runs in an isolated Docker container. Make sure to properly edit the values in the code and familiarize yourself with the tools being used.

### Prerequisites
Before you begin editing the code, you should have following technologies installed and working. Links to proper documentation is included. It is recommended to have atleast done the official tutorials before continuing.

| Tool | Resource |
| --- | --- |
| Airflow | [Quick Start](https://airflow.apache.org/docs/apache-airflow/stable/start.html) | 
| Docker | [Get Started](https://docs.docker.com/get-started/) |
| Google Cloud CLI | [CLI install](https://cloud.google.com/sdk/docs/install) |
| Google Cloud Auth | [Google Authentication](https://cloud.google.com/docs/authentication) |
| Terraform | [GCP Get Started](https://developer.hashicorp.com/terraform/tutorials/gcp-get-started) |
| Spotify | [Web API](https://developer.spotify.com/documentation/web-api)

### Variables
Following snippets showcase some variables needed in order for the DAG to run sucessfully.
```env
# Google
GOOGLE_APPLICATION_CREDENTIALS="/path/to/google/credentials/json"
...

# Spotify
SPOTIFY_AF_ID="your-app-client-id"
SPOTIFY_AF_SECRET="your-app-client-secret"
...
```
The `.env` requires access to your GCP credentials and Spotify Apps ID and key. The Google Cloud credntials allow for access into cloud applications and lets you call client libraries such as `Cloud Storage` and `BigQuery`. While the Sptofy App IDs and keys allows for requesting an access token in order to establish a server-to-server connection with Spotify's API. An example snippet of using the `Cloud Storage` client is showcased below. Variables in need of developer input is documented in the code for easier localization.

```python
import pandas as pd
from google.cloud import storage

def load_to_storage(df: pd.DataFrame, country: str, date: str) -> None:
    """
    Uploads a parquet file to GCS bucket.
    """
    # Construct a Storage client object.
    client = storage.Client()
    
    # TODO(developer): set bucket_name to the ID of your GCS bucket.
    # bucket_name = "your-bucket-name"

    # TODO(developer): set the destination_blob to the ID of your GCS object.
    # destination_blob = "storage-object-name"

    bucket = client.bucket(bucket_name)
    bucket.blob(destination_blob).upload_from_string(
        df.to_parquet(index=False), content_type=None
    )

    print(
        f"File {country}-{date}.parquet uploaded to Bucket {bucket_name}/featured/{date}"
    )
    return
```

### Tasks
The Project runs a single DAG instance daily and is intitially divided into 4 `upstream` tasks (1 task per region). The `upstream` tasks extract the data from the Spotify Web API, when they finish the following `downstream` tasks complete the dag by loading the data into the cloud. The `downstream` rely on the upstream to complete before loading the data into Cloud Storage and then BigQuery.
![DAG graph made with Lucid Chart](https://github.com/blktheta/spotify-image/blob/925acccfed0f728a93b6ab2613b7fa7721f509ce/images/dag-graph.png "Airflow DAG graph")

# The Result
Sample text.

![Spotify infographic made with Canva](https://github.com/blktheta/spotify-image/blob/15ea4176a3c5285950b64a08309a3afe7a25fd9b/images/case1.png "Spotify Study infographic")

![Spotify infographic made with Canva](https://github.com/blktheta/spotify-image/blob/15ea4176a3c5285950b64a08309a3afe7a25fd9b/images/case2.png "Spotify Study infographic")

![Spotify infographic made with Canva](https://github.com/blktheta/spotify-image/blob/15ea4176a3c5285950b64a08309a3afe7a25fd9b/images/case3.png "Spotify Study infographic")

![Spotify infographic made with Canva](https://github.com/blktheta/spotify-image/blob/15ea4176a3c5285950b64a08309a3afe7a25fd9b/images/case4.png "Spotify Study infographic")

![Spotify infographic made with Canva](https://github.com/blktheta/spotify-image/blob/15ea4176a3c5285950b64a08309a3afe7a25fd9b/images/case5.png "Spotify Study infographic")

![Spotify infographic made with Canva](https://github.com/blktheta/spotify-image/blob/15ea4176a3c5285950b64a08309a3afe7a25fd9b/images/case6.png "Spotify Study infographic")

## Spotify Playlist
[Link to the Top 100 Featured tracks, inbetween 20230524 - 20230530.](https://open.spotify.com/playlist/7sV5on10eXq4GCOfFfqLlD?si=eb3db9a9b5d14170&nd=1)

# Summary
Sample text.

## Future Revisions
Extended Scope.
