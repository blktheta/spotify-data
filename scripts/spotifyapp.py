import os
import pandas as pd

from spotifyclient import SpotifyClient
from spotifydata import SpotifyData
from spotifyregion import SpotifyRegion

class SpotifyApp:
    """
    Create an application that extracts the data from the Spotify Web API.

    region  = Set the region to specify which countries 
            the app will extract data from.
            Options:
            -- AF = Africa
            -- AS = Asia
            -- EU = Europe
            -- NASAOC = North America, South America and Oceania
    """

    def __init__(self, region: str) -> None:
        self.client = SpotifyClient(region) # Makes the API requests.
        self.data = SpotifyData()           # Perfroms the filtering.
        self.region = SpotifyRegion(region) # Maps selected countries.
        return

    def extract_data(self, country: str, date: str) -> pd.DataFrame:
        """
        Main extraction script.
        
        Send GET requests to the Spotify client that respond 
        with data in json format. Which are later filterd to 
        create a sample based on preference and stored in a
        pandas dataframe. 

        The 4 dataframes are:
        featured_playlist   = stores data about country, date 
                            and time in which the playlists 
                            were featured in the Spotify region.
        
        playlists   = stores general data about the playlist,
                    as well as a list of featured tracks.

        tracks  = stores general data about the track, as well
                as info about the artist and album.

        audio_features  = stores data about the track's nature 
                        in terms of audio quallity.
        """
        df_fp = self.extract_featured_playlists(country, date)
        
        # Insert country and region columns 
        # based on ISO code of df column.
        df_fp["country"] = df_fp["iso"].map(
            self.region.country_names, na_action="ignore"
        )
        df_fp["region"] = df_fp["iso"].map(
            self.region.country_regions, na_action="ignore"
        )

        # Filter out duplicate playlist IDs 
        # before extracting playlist data.
        df_p = self.extract_playlists(df_fp["playlist_id"].unique())

        # Retrieve the list of tracks for each 
        # unique playlist featured. Extract 
        # tracks that appear on featured playlist.
        t_data = list()
        p_data = dict(zip(df_p["playlist_id"], df_p["playlist_tracks_ids"]))
        for key, value in p_data.items():
            df = self.extract_tracks(value)
            t_data.append(df.assign(playlist_id=key))
        df_t = pd.concat(t_data)

        # Filter out duplicate track IDs 
        # before extracting audio data.
        df_af = self.extract_audio_features(df_t["track_id"].unique())

        # Merge dataframes.
        merged_p = df_fp.merge(df_p, left_on="playlist_id", right_on="playlist_id")
        merged_t = df_t.merge(df_af, left_on="track_id", right_on="track_id")
        df_merged = (
            merged_t.merge(merged_p, left_on="playlist_id", right_on="playlist_id")
            .drop(columns=["playlist_tracks_ids"])
            .reset_index(drop=True)
            .sort_index(axis=1)
        )

        return self.convert_dtypes(df_merged)   # Convert to parquet datatypes.

    # Extraction methods.
    def extract_featured_playlists(self, country: str, date: str) -> pd.DataFrame:
        """
        Extract data from the API featured playlist endpoint.
        """
        sample_list = list()
        for hour in range(0, 24):
            timestamp = f"{date}T{hour:02d}:00:00"
            response_json = self.client.get_featured_playlists(country, timestamp)
            sample = self.data.transform_featured_playlists(
                response_json, country, timestamp
            )
            sample_list.append(pd.DataFrame(sample))
        return pd.concat(sample_list)

    def extract_playlists(self, playlist_ids: list) -> pd.DataFrame:
        """
        Extract data from Spotify playlist endpoint.
        """
        sample_list = list()
        for playlist_id in playlist_ids:
            response_json = self.client.get_playlists(playlist_id)
            sample = self.data.transform_playlists(response_json)
            sample_list.append(pd.DataFrame(sample))
        return pd.concat(sample_list)

    def extract_tracks(self, track_ids: list) -> pd.DataFrame:
        """
        Extract data from Spotify several tracks endpoint.
        """
        sample_list = list()
        for i in range(0, len(track_ids), 50):
            query = ",".join(track_ids[i : i + 50])
            response_json = self.client.get_tracks(query)
            sample = self.data.transform_tracks(response_json)
            sample_list.append(pd.DataFrame(sample))
        return pd.concat(sample_list)

    def extract_audio_features(self, track_ids: list) -> pd.DataFrame:
        """
        Extract data from Spotify audio features endpoint.
        """
        sample_list = list()
        for i in range(0, len(track_ids), 100):
            query = ",".join(track_ids[i : i + 100])
            response_json = self.client.get_audio_features(query)
            sample = self.data.transform_audio_features(response_json)
            sample_list.append(pd.DataFrame(sample))
        return pd.concat(sample_list)

    def convert_dtypes(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Assign preferred Parquet datatypes to dataframe.
        """
        df["featured"] = pd.to_datetime(df["featured"], errors="coerce")
        df["track_album_release"] = pd.to_datetime(df["track_album_release"], errors="coerce").dt.date
        return df.astype(
            {
                "region": "string",
                "iso": "string",
                "country": "string",
                "playlist_id": "string",
                "playlist_name": "string",
                "playlist_followers_total": "int32",
                "playlist_tracks_total": "int32",
                "track_id": "string",
                "track_name": "string",
                "track_popularity": "int32",
                "track_duration": "int32",
                "track_explicit": "bool",
                "track_artist_id": "string",
                "track_artist_name": "string",
                "track_album_id": "string",
                "track_album_name": "string",
                "track_album_type": "string",
                "track_audio_acousticness": "float32",
                "track_audio_danceability": "float32",
                "track_audio_energy": "float32",
                "track_audio_instrumentalness": "float32",
                "track_audio_liveness": "float32",
                "track_audio_loudness": "float32",
                "track_audio_mode": "int32",
                "track_audio_speechiness": "float32",
                "track_audio_tempo": "int32",
                "track_audio_time_signature": "int32",
                "track_audio_tonality": "int32",
                "track_audio_valence": "float32",
            },
            errors="ignore",
        )
