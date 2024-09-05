import re
from pathlib import Path

from tangram.bin.common import make_target_path

DOWNLOADS_PATH = Path('/home/teo/Downloads')
DESTINATION_PATH = Path('/home/teo/_teos_gdrive/fun/tangram/individual-tangram-builder/solutions')

EXT = "png"
# %%


def downloads_to_solution_dir():
    # %%
    paths = list(DOWNLOADS_PATH.glob(f"*.{EXT}"))
    print( f"paths has {len(paths)}")

    source_paths = [ path for path in paths if re.match( r"tangram ?\(\d+\).png", path.name ) ]
    print( f"tangrams has {len( source_paths)}" )

    for source_path in source_paths:
        target_path = make_target_path(source_path, DESTINATION_PATH)

        print( str(source_path), f"\n \t=> {target_path}" )
        source_path.rename(target_path)
    # %%



if __name__ == "__main__":
    downloads_to_solution_dir()
