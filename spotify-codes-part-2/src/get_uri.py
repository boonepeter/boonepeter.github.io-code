import requests

def get_uri(media_ref: int, token):
    head = {
        "X-Client-Id": "58bd3c95768941ea9eb4350aaa033eb3",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "close",
        "App-Platform": "iOS",
        "Accept": "*/*",
        "User-Agent": "Spotify/8.5.68 iOS/13.4 (iPhone9,3)",
        "Accept-Language": "en",
        "Spotify-App-Version": "8.5.68",
        "Authorization": f"Bearer {token}"
    }
    url = f'https://spclient.wg.spotify.com:443/scannable-id/id/{media_ref}?format=json'
    response = requests.get(url, headers=head)
    response.raise_for_status()
    return response.json()

def get_info(uri, token):
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
    json = response.json()
    result = {
        "name": json["name"]
    }
    if "artists" in json:
        result['artists'] = []
        for a in json['artists']:
            result["artists"].append(a["name"])
    if "album" in json:
        result['album'] = json['album']['name']

    if "description" in json:
        result["description"] = json['description']

    return result

