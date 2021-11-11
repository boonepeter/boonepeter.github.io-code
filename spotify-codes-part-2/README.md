# Spotify Codes Part 2

## Install packages

```bash
pip3 install -r requirements.txt
```

## Run

```bash
python decode_barcode.py --token="YOUR_TOKEN_HERE" ./pics/spotify_playlist_37i9dQZF1DXcBWIGoYBM5M.jpg
```

## Token

This script requires your authorization token to run. You can get this (manually) by visiting [Spotify's Web client](https://open.spotify.com/). If you inspect the page source (F12), you can search for `access_token` in the Network tab after reloading the page. Copy the value and paste it into the `--token` argument.

## Output

```bash
Heights: [0, 6, 0, 2, 4, 5, 1, 4, 5, 2, 3, 7, 3, 7, 1, 5, 6, 2, 5, 7, 4, 3, 0]
Media ref: 57268659651
URI: spotify:user:spotify:playlist:37i9dQZF1DXcBWIGoYBM5M
Summary:
{
  'description': 'Coldplay & BTS are on top of the Hottest 50!',
  'name': "Today's Top Hits",
  'type': 'playlist',
  'url': 'https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M'
}
```
