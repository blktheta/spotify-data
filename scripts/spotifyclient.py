import base64
import os
import requests
import time


class SpotifyClient(requests.Session):
    """
    Create authorized server-to-server connection with the Spotify Web API.

    The authorization flow used for this application is 'Client credentails'.

    Further details can be read @Spotify:
    https://developer.spotify.com/documentation/web-api/concepts/authorization

    Note: as of '2023-05-26' requesting data from all regions in a single
    Spotify app will lead to exceeding Spotify's rate limits.
    The current solution divides the extraction between multiple apps,
    further divisions can be made if required.
    """

    def __init__(self, region: str) -> None:
        super().__init__()
        self.client_id = os.environ[f"SPOTIFY_{region}_ID"]
        self.client_secret = os.environ[f"SPOTIFY_{region}_SECRET"]
        self.tkn_url = "https://accounts.spotify.com/api/token"
        self.api_url = "https://api.spotify.com/v1"
        self.request_authorization()  # Make API request.
        return

    def request_authorization(self) -> None:
        """
        Retrieve the client token credentials from the API.
        """
        # Encode (base64) string that contains
        # client ID and client secret key.
        auth_string = f"{self.client_id}:{self.client_secret}"
        auth_bytes = auth_string.encode("utf-8")
        auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

        # Header and body config for token API request.
        header = {
            "Authorization": "Basic " + auth_base64,
            "Content-Type": "application/x-www-form-urlencoded",
        }
        body = {"grant_type": "client_credentials"}

        response = self.request_token(header, body)
        access_token = response.json()["access_token"]  # Expires in 3600 seconds
        self.headers.update({"Authorization": "Bearer " + access_token})

        print(f"Access token(3600 seconds): {access_token}")
        return

    def request_token(
        self, header: dict, body: dict, retry: int = 3
    ) -> requests.Response:
        """
        Send a POST request to the /api/token endpoint.
        """
        while retry > 0:
            try:
                # Make an API request
                response = self.post(self.tkn_url, headers=header, data=body)
            except requests.exceptions.ConnectionError as connection_error:
                print("Connection error occured while requesting for access token.")
            else:
                print("Finished requesting for access token.")
                return response
            retry -= 1

            # When requesting for a new access token the
            # connection to the server will need to refresh/update
            # 30 seconds between the calls should suffice.
            print("Sleeping for 30 seconds before retrying the token request.")
            time.sleep(30)
        else:
            raise RuntimeError("Max retries exceeded while requesting token, aborting.")

    def request_endpoint(self, url: str, retry: int = 3) -> requests.Response:
        """
        Send a GET request to the url endpint.
        """
        while retry > 0:
            # Optional: limit the requests made to the API
            # by adjusting the sleep time inbetween requests.
            # Max: ~3 requests per second (180 per minute).
            time.sleep(400 / 1000)

            try:
                # Make an API request
                response = self.get(url)
                response.raise_for_status()
            except requests.exceptions.HTTPError as http_error:
                status_code = http_error.response.status_code
                print(f"HTTP error {status_code} occured while requesting data.")

                if status_code == 401:
                    print("Bad or expired token, refreshing.")
                    # Make an API rquest to refresh the client credentials
                    self.request_authorization()

                if status_code == 429:
                    wait_period = int(response.headers["retry-after"])
                    print(
                        f"Retry after: {wait_period} seconds ({(wait_period/60)/60} hours)"
                    )

                    if wait_period > 82800:  # 23 hours
                        raise RuntimeError("Exceeded rate limits, aborting.")

                    for i in range(wait_period, 0, -1):  # Countdown
                        time.sleep(1)
                        print(f"Sleeping for {i:05d} seconds", end="\r")
                    # Make an API rquest to refresh the client credentials
                    self.request_authorization()
            except requests.exceptions.ConnectionError as connection_error:
                print("Connection error occured while requesting data.")
            else:
                print(f"Finished requesting data from endpoint:\n{url}")
                return response
            retry -= 1
        else:
            raise RuntimeError("Max retries exceeded while requesting data, aborting.")

    def get_featured_playlists(self, country: str, timestamp: str) -> dict:
        """
        Get a list of Spotify featured playlists in json format.
        """
        url = f"{self.api_url}/browse/featured-playlists?country={country}&timestamp={timestamp}&limit=50"
        return self.request_endpoint(url).json()

    def get_playlists(self, playlist_id: str) -> dict:
        """
        GET a playlist owned by a Spotify user.
        """
        url = f"{self.api_url}/playlists/{playlist_id}"
        return self.request_endpoint(url).json()

    def get_tracks(self, track_ids: str) -> dict:
        """
        GET information for multiple tracks based on their Spotify IDs.
        """
        url = f"{self.api_url}/tracks?ids={track_ids}"
        return self.request_endpoint(url).json()

    def get_audio_features(self, track_ids: str) -> dict:
        """
        GET audio features for multiple tracks based on their Spotify IDs.
        """
        url = f"{self.api_url}/audio-features?ids={track_ids}"
        return self.request_endpoint(url).json()
