# On this page
* [Purpose](#purpose)
* [Scope](#scope)
* [Infrastructure](#infrastructure)
  * [The Data Stack](#the-data-stack)
  * [Extrack and Load](#extrack-and-load)
    * [Data Source](#data-source)
  * [Orchestration](#orchestration)
  * [Data Warehouse](#data-warehouse)
    * [Data Storage](#data-storage)
  * [Transformation](#transformation)
    * [Nested and Repeated Structures](#nested-and-repeated-structures)
  * [Vizuallization](#vizuallization)
* [Python Guide](#python-guide)
  * [Prerequisites](#prerequisites)
  * [Variables](#variables)
  * [Tasks](#tasks)
* [The Result](#the-result)
  * [Case 1](#case-1)
  * [Case 2](#case-2)
  * [Case 3](#case-3)
  * [Case 4](#case-4)
  * [Case 5](#case-5)
  * [Case 6](#case-6)
  * [Spotify Playlists](#spotify-playlists)
* [Summary](#summary)
  * [Future Revisions](#future-revisions)

| NOTE: This is a Proof of Concept Documentation |
| :--- | 
| This project is meant for cloud development. It acts as a proof of concept for what can be done with the Spotify Web API. The configuration supports basic configuration using environment variables or an .env file. Feel free to modify this project to suit your needs. |

# Purpose
The goal of this project is to highlight the songs that Spotify recommend in their official playlists and what character said songs possess. The data will help upcoming artist understand the Spotify market audience and better target their efforts. This project also conceptually describes on high level the componenents which all together are defined as an ELT data pipeline.  

# Scope
The project is limited to a weeks worth of data (~30 million rows of data) for brevity. The DAG however should return ~1.5 billion rows of data annually. This document is limited to describe the pipeline conceptually, as there are other resources that describe it in more detail.

# Infrastructure
## &#x2263; The Data Stack
![Data stack made in Canva](https://github.com/blktheta/spotify-image/images/data-stack.png "ELT data stack")

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

## &#x21C4; Extrack and Load
The project use custom made pipeline built in `Python 3.10` and orchestrated in `Airflow 2.5.3` run in a `Docker` container. This ELT pipeline requires the owner to be responsible for building, maintaining, or orchestrating the movement of data from the data source into the data warehouse.

### Data Source
The RAW data loaded into the data warehouse comes from the [Spotify Web API](https://developer.spotify.com/documentation/web-api). The data runs though an Airflow pipeline and is stored raw in Google Cloud Storage. The *Replication Frequency* (RF) is set to 24h and *Service Level Objective* (SLO) to 3 hours. The numbers may change if Spotify updates their rate limits in near future. 

## &#x23F2; Orchestration
This pipeline use Airflow on a Docker container for orchestration. The specific setup can be found in the `docker-compose.yaml` file. It is based on the offical `docker-compose.yaml` file fetched from the Airflow documentation [here](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html). 

## &#x2601; Data Warehouse
The project use Google Cloud Storage as data warehouse. Its seamless integration with other GC features and the 90 days trial makes it a great contendor for smaller projects.

### Data Storage
The project use two primary databases `raw` and `prep`, a third `prod` database could be used to further transform and model the data for business use. The `raw` database is where data is first loaded into Cloud Storage; the `prep` database is controlled by BigQuery and is for data that is ready for analysis. 

## &#x21BA; Transformation
The project use Google Cloud BigQuery for all `prep` transformation. The data modeling follow a star schema, with a *denormalized* "fact" table, rather then *normalized* dimension tables. The star schema supports analytical queries better for it allows the use of running simpler queries because the limited number of joins. It also performs faster aggregations that improve the query performance.  

![Star schema made in Lucid Chart](https://github.com/blktheta/spotify-image/blob/248b34dee8a0417c64ca91800276bc251f42e272/images/star-schema.png "Denormalized star schema")

### Nested and Repeated Structures
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
|  |  |  |  |  | Under någon ny | Miriam Bryant | ... |
|  |  |  | Made in Sweden | Måndagsbarn | Olivia Lobato | Måndagsbarn | ... |
|  |  |  |  |  | 5D | Lykke Li | ... |
|  |  |  |  |  | Superstar | Bianca Ingrosso | ... |
| 2023-05-24 | Asia | Korea | Dalkom Cafe | Mirror | Sunday Moon | ... |
|  |  |  |  |  | Sell My Heart | Junggigo | ... |
|  |  |  | Soundtracks | Photo of My Mind | Song Ga In | ... |
| 2023-05-24 | Africa | Nigeria | Hot Hits Naija | It's Plenty | Burna Boy | ... |

## &#x25D4; Visuallization
The project use Google Cloud Looker Studio as a data visualization tool. A sample report is appended to the project to showcase the simple usage of the `prep` data. 

# Python Guide
Sample text.

## Prerequisites
Sample text.

## Variables
Sample text.

## Tasks
Sample text.

# The Result
Sample text.

## Case 1
Sample text.

## Case 2
Sample text.

## Case 3
Sample text.

## Case 4
Sample text.

## Case 5
Sample text.

## Case 6
Sample text.

## Spotify Playlists
Sample text.

# Summary
Sample text.

## Future Revisions
Extended Scope.
