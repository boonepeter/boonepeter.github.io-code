from typing import Tuple
import requests

HEADERS_LUT = {
    "X-Client-Id": "58bd3c95768941ea9eb4350aaa033eb3",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "close",
    "App-Platform": "iOS",
    "Accept": "*/*",
    "User-Agent": "Spotify/8.5.68 iOS/13.4 (iPhone9,3)",
    "Accept-Language": "en",
    "Spotify-App-Version": "8.5.68",
}
MEDIA_REF_LUT_URL = "https://spclient.wg.spotify.com:443/scannable-id/id"

def get_uri(media_ref: int, token: str):
    """Query Spotify internal API to get the URI of the media reference."""
    header = {
        **HEADERS_LUT,
        "Authorization": f"Bearer {token}"
    }
    url = f'{MEDIA_REF_LUT_URL}/{media_ref}?format=json'
    response = requests.get(url, headers=header)
    response.raise_for_status()
    return response.json()

def get_info(uri: str, token: str) -> Tuple[dict, dict]:
    """Query the Spotify API to get information about a URI."""
    info_headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {token}"
    }
    split = uri.split(":")
    content_type = split[-2] + "s"
    id = split[-1]
    response = requests.get(f"https://api.spotify.com/v1/{content_type}/{id}", headers=info_headers)
    response.raise_for_status()
    resp = response.json()
    result = {
        "name": resp["name"],
        "type": split[-2],
        "url": resp["external_urls"]["spotify"],
    }
    if "artists" in resp:
        result['artists'] = []
        for a in resp['artists']:
            result["artists"].append(a["name"])
    if "album" in resp:
        result['album'] = resp['album']['name']

    if "description" in resp:
        result["description"] = resp['description']
    
    return result, resp

