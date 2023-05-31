class SpotifyData:
    """
    External application that uses retrieved Spotify content,
    such as song data, audio data and playlists, to filter our
    information.

    What information to keep  is decided on preference, availability and
    analytic intention. A more detailed descritpion of what  information 
    there is to extract can be found @Spotify. Links (as of 2023-05-26).
    
    https://developer.spotify.com/documentation/web-api/reference/get-featured-playlists

    https://developer.spotify.com/documentation/web-api/reference/get-playlist

    https://developer.spotify.com/documentation/web-api/reference/get-several-tracks

    https://developer.spotify.com/documentation/web-api/reference/get-several-audio-features
    """

    def __init__(self) -> None:
        return

    def transform_featured_playlists(
        self, j: dict, country: str, timestamp: str
    ) -> dict:
        """
        Chose what information to extract from the featured playlist endpoint.
        """
        return {
            "playlist_id": (f["id"] for f in j["playlists"]["items"] if f),
            "iso": country,
            "featured": timestamp,
        }

    def transform_playlists(self, j: dict) -> dict:
        """
        Chose what information to extract from the playlist endpoint.
        """
        return {
            "playlist_id": j["id"],
            "playlist_name": j["name"],
            "playlist_followers_total": j["followers"]["total"],
            "playlist_tracks_total": j["tracks"]["total"],
            "playlist_tracks_ids": [
                [p["track"]["id"] for p in j["tracks"]["items"] if p["track"]]
            ],
        }

    def transform_tracks(self, j: dict) -> dict:
        """
        Chose what information to extract from the tracks endpoint.
        """
        return {
            "track_id": (t["id"] for t in j["tracks"] if t),
            "track_name": (t["name"] for t in j["tracks"] if t),
            "track_popularity": (t["popularity"] for t in j["tracks"] if t),
            "track_duration": (int(t["duration_ms"] / 1000) for t in j["tracks"] if t),
            "track_explicit": (t["explicit"] for t in j["tracks"] if t),
            "track_artist_id": (t["artists"][0]["id"] for t in j["tracks"] if t),
            "track_artist_name": (t["artists"][0]["name"] for t in j["tracks"] if t),
            "track_album_id": (t["album"]["id"] for t in j["tracks"] if t),
            "track_album_name": (t["album"]["name"] for t in j["tracks"] if t),
            "track_album_release": (
                t["album"]["release_date"] for t in j["tracks"] if t
            ),
            "track_album_type": (t["album"]["type"] for t in j["tracks"] if t),
        }

    def transform_audio_features(self, j: dict) -> dict:
        """
        Chose what information to extract from the audio features endpoint.
        """
        return {
            "track_id": (a["id"] for a in j["audio_features"] if a),
            "track_audio_danceability": (
                a["danceability"] for a in j["audio_features"] if a
            ),
            "track_audio_energy": (a["energy"] for a in j["audio_features"] if a),
            "track_audio_tonality": (a["key"] for a in j["audio_features"] if a),
            "track_audio_loudness": (a["loudness"] for a in j["audio_features"] if a),
            "track_audio_mode": (a["mode"] for a in j["audio_features"] if a),
            "track_audio_speechiness": (
                a["speechiness"] for a in j["audio_features"] if a
            ),
            "track_audio_acousticness": (
                a["acousticness"] for a in j["audio_features"] if a
            ),
            "track_audio_instrumentalness": (
                a["instrumentalness"] for a in j["audio_features"] if a
            ),
            "track_audio_liveness": (a["liveness"] for a in j["audio_features"] if a),
            "track_audio_valence": (a["valence"] for a in j["audio_features"] if a),
            "track_audio_tempo": (a["tempo"] for a in j["audio_features"] if a),
            "track_audio_time_signature": (
                a["time_signature"] for a in j["audio_features"] if a
            ),
        }
