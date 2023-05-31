import sys
import pandas as pd

from google.cloud import storage
from spotifyapp import SpotifyApp


def load_to_storage(
    client: storage.Client, df: pd.DataFrame, country: str, date: str
) -> None:
    """
    Uploads a parquet file to GCS bucket.

    Parquet file naming convention is derived from
    the country ISO code and date of featured data.
    File name convention = 'ISO-YYYYMMDD.parquet'

    The folder structure in GCS bucket organised by date.
    Folder name convention = 'featured/YYYYMMDD'
    """
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


def enable_filtering(
    client: storage.Client, app: SpotifyApp, date: str, enable: bool = False
) -> list:
    """
    Filter our previously collected data by comparing ISO codes
    in file names. Return a list with ISO codes to base the
    extraction script on.

    prefix  = Lists all the blobs in the bucket that begin with the prefix.
            This can be used to list all blobs in a "folder", e.g. "public/".
    """
    # TODO(developer): set bucket_name to the ID of your GCS bucket.
    # bucket_name = "your-bucket-name"

    # TODO(developer): set prefix to restrict the results to given "folder".
    # prefix = "path/to/folder"

    if enable:
        blobs = client.list_blobs(bucket_name, prefix=prefix)

        # Retrieve the iso code of previously stored parquet files.
        # Blob path = featured/YYYYMMDD/iso-YYYYMMDD.parquet
        blob_names = [blob.name[18:20] for blob in blobs]
        print(
            f"Country ISO codes already stored in GCS Bucket {bucket_name}: {blob_names}"
        )

        # Save regional iso code that have yet to be stored in GCS bucket.
        country_codes = [c for c in app.region.country_codes if c not in blob_names]

    if not enable:
        # Ask for all ISO code in the regions,
        # this will overwrite previously collected files.
        country_codes = app.region.country_codes

    print(f"Extracting data from following countries(ISO): {country_codes}")
    return country_codes


def main(region: str, date: str) -> None:
    """
    Run script.

    region  = Set the region to specify which countries
            the script will extract data from.
            Options:
            -- AF = Africa
            -- AS = Asia
            -- EU = Europe
            -- NASAOC = North America, South America and Oceania

    date    = Set the date(YYYY-MM-DD) to specify from
            which date the script will extract data.
    """
    # Construct a Spotify app object.
    app = SpotifyApp(region)

    # Construct a GC Storage client object.
    client = storage.Client()

    # Optional(developer): set enable to True
    # if you want to filter out previously
    # collected data from the current run script.
    country_codes = enable_filtering(client, app, date, enable=True)

    for country in country_codes:
        # Extract and save data into a Pandas DataFrame object.
        df = app.extract_data(country, date)
        print(df.info(verbose=True))

        # Load DataFrame as a Parquet file directly into your GCS Bucket.
        load_to_storage(client, df, country, date.replace("-", ""))

    print(
        f"Extraction script for region {region} on date {date} finished successfully."
    )
    return


if __name__ == "__main__":
    main(
        region=sys.argv[1].upper(),
        date=sys.argv[2],
    )
