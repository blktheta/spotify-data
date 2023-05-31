import datetime
import sys

from google.cloud import bigquery


def load_to_table(date: str) -> None:
    """
    Load multiple files from GC Storage bucket to a BigQuery table.
    """
    # Construct a BigQuery client object.
    client = bigquery.Client()

    # TODO(developer): set source_uri to the GCS bucket folder to create table from.
    # source_path = "gs://your-bucket-name/path/to/folder/*"

    # TODO(developer): set table_id to the ID of the table to create.
    # table_id = "your-project-id.your_dataset.your_table_name"

    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.PARQUET,
    )

    load_job = client.load_table_from_uri(
        source_uri, table_id, job_config=job_config
    )  # Make an API request.

    load_job.result()  # Waits for the job to complete.

    destination_table = client.get_table(table_id)

    # Opional: set table to expire 3 days from now.
    """
    expiration = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(
        days=3
    )

    destination_table.expires = expiration
    client.update_table(destination_table, ["expires"])  # API request.
    """
    print(f"Data uploaded from {source_uri} to Bigquery table {table_id}")
    return


if __name__ == "__main__":
    load_to_table(
        date=sys.argv[1],
    )
