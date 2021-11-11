import argparse
import pprint
from get_heights import get_heights
from encode_decode import spotify_bar_decode
from get_uri import get_uri, get_info


parser = argparse.ArgumentParser(description="Spotify Barcode Decoder.")

parser.add_argument("filename", help="The filename of the barcode to decode.")
parser.add_argument("--token", required=True, help="Your Spotify authorization token.")



if __name__ == "__main__":
    args = parser.parse_args()
    filename = args.filename
    token = args.token
    heights = get_heights(filename)
    print(f"Heights: {heights}")
    # drop the fist, last, and 12th bar
    heights = heights[1:11] + heights[12:-1]
    decoded = spotify_bar_decode(heights)
    print(f"Media ref: {decoded}")
    uri = get_uri(decoded, token)
    print(f"URI: {uri['target']}")
    summary, full_response = get_info(uri["target"], token)
    print("Summary:")
    pprint.pprint(summary)

