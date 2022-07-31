from pathlib import Path
import datetime as dt
import re
DOWNLOADS_PATH = Path('/home/mateo/Downloads')
DESTINATION_PATH = Path('/home/mateo/_teos_gdrive/fun/tangram/individual-tangram-builder/')

EXT = "png"
# %%


def _main():
    # %%
    paths = list(DOWNLOADS_PATH.glob(f"*.{EXT}"))
    print( f"paths has {len(paths)}")

    tangrams = [ path for path in paths if re.match( r"tangram ?\(\d+\).png", path.name ) ]
    print( f"tangrams has {len( tangrams )}" )
    # %%
    for tang in tangrams:
        create_dt = dt.datetime.fromtimestamp( tang.lstat().st_ctime )
        tstamp_str = create_dt.isoformat().replace(':', '')[:-3]
        new_path = DESTINATION_PATH / f"tangram - {tstamp_str}.png"
        print( str(tang), f"\n \t=> {new_path}" )
        tang.rename(new_path)
    # %%