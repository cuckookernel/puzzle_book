import datetime as dt
from hashlib import sha256
from pathlib import Path

import numpy as np

PZLS_PATH = Path( "/home/teo/_teos_gdrive/fun/tangram/individual-tangram-builder/puzzles" )
SOLS_PATH = Path( "/home/teo/_teos_gdrive/fun/tangram/individual-tangram-builder/solutions" )
SOLS_PATTERN = "tangram - *.png"
PUZZLE_SUFFIX = ".puzzle.png"


Array = np.ndarray


def make_target_path(input_path: Path, dest_dir: Path, add_hash: bool = False) -> Path:

    create_dt = dt.datetime.fromtimestamp(input_path.lstat().st_ctime)
    tstamp_str = create_dt.isoformat().replace(':', '')[:-3]

    if add_hash:
        _hash = '.' + sha256(input_path.read_bytes()).hexdigest()[:16]
    else:
        _hash = ''

    target_path = dest_dir / f"tangram - {tstamp_str}{_hash}.png"

    return target_path
# %%
