from get_heights import get_heights
from encode_decode import spotify_bar_decode
from get_uri import get_uri, get_info
import sys

token = "BQCeRf_QYRKMCwt3sLNKvNlTGNUsHNnp8InJAyRpUWU-PEZ-vu5TXqlWle_kY9z_TcVUSz0xlhaFJd6QWdt4g_n-xPzGwVUTft86yg_eU_6k_DDRCVtS6q9N_OW3r5j_Cxc8oQIzhiaK6Jg3c2F73VrnUBOJW7P-nv9Qiw5e--nc_45vs0A80FOIdqFgqUDXE6znsHsg_x0w_nbA6WPTS2d72KkhnmCdWj34HAD9y8qShGOotDWy5v78wrHEviwCf1TuNgiXUcO5dDPCJ6MNKxaq0WRA6Q"

if __name__ == "__main__" and len(sys.argv) > 1:
    path = sys.argv[1]
    if len(sys.argv) > 2:
        token = sys.argv[2]
    heights = get_heights(path)
    print(f"Heights: {heights}")
    # drop the fist, last, and 12th bar
    heights = heights[1:11] + heights[12:-1]
    decoded = spotify_bar_decode(heights)
    print(f"Media ref: {decoded}")
    uri = get_uri(decoded, token)
    print(f"URI: {uri['target']}")
    info = get_info(uri["target"], token)
    print("Information:")
    print(info)
