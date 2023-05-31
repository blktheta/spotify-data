import sys

from google.cloud import bigquery


def insert_to_table(date: str) -> None:
    """
    Performs an 'INSERT INTO' query with BigQuery.

    Inserts previously extracted date from 'source_table' to
    the destination_table (collective data table). The main
    table is denormalized and includes nested-repeated columns.
    It is also partitioned by 'featured'(date) column and
    clustered by 'region' then 'iso' columns.
    """
    # Construct a BigQuery client object.
    client = bigquery.Client()

    # TODO(developer): set source_table to the ID of the table to extract from.
    # source_table = "your-project-id.your_dataset.your_table_name"

    # TODO(developer): set destination_table to the ID of the table to insert into.
    # destination_table = "your-project-id.your_dataset.your_table_name"

    query = f"""
        INSERT INTO {destination_table}(
            featured,
            region,
            iso,
            country,
            playlist
        )
        SELECT
            featured,
            region,
            iso,
            country,
            [STRUCT(
                playlist_id,
                playlist_name,
                playlist_followers_total,
                playlist_tracks_total,
                [STRUCT(
                    track_id,
                    track_name,
                    track_popularity,
                    track_duration,
                    track_explicit,
                    STRUCT(
                        track_artist_id,
                        track_artist_name
                    ),
                    STRUCT(
                        track_album_id,
                        track_album_name,
                        track_album_type,
                        track_album_release
                    ),
                    STRUCT(
                        track_audio_acousticness,
                        track_audio_danceability,
                        track_audio_energy,
                        track_audio_instrumentalness,
                        track_audio_liveness,
                        track_audio_loudness,
                        track_audio_mode,
                        track_audio_speechiness,
                        track_audio_tempo,
                        track_audio_time_signature,
                        track_audio_tonality,
                        track_audio_valence
                    )
                )]
            )]
        FROM {source_table};
    """

    query_job = client.query(query)  # Make an API request.

    print(
        f"Table {source_table} was successfully inserted into table {destination_table}"
    )
    return


if __name__ == "__main__":
    insert_to_table(
        date=sys.argv[1],
    )
