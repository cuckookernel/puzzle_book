
from typing import List
from pathlib import Path
from collections import Counter
import numpy as np

import cv2

SOLS_PATH = Path( "/home/mateo/_teos_gdrive/fun/tangram/individual-tangram-builder/" )
SOLS_PATTERN = "tangram - *.png"
PUZZLES_PATH = SOLS_PATH / "tangram-puzzles"
PUZZLE_SUFFIX = ".solution.png"

Array = np.ndarray
# %%


def _main():
    # %%
    PUZZLES_PATH.mkdir(exist_ok=True, parents=True)
    paths = list( SOLS_PATH.glob(SOLS_PATTERN) )
    # %%
    for path in paths:
        out_path = PUZZLES_PATH / (path.stem + PUZZLE_SUFFIX)
        print( path.stem )
        img = cv2.imread( str( path ), cv2.IMREAD_UNCHANGED )

        img2 = _convert_to_puzzle(img)
        cv2.imwrite( str( out_path ), img2 )
    # %%


def _interactive_testing(paths: List[Path]):
    # %%
    path = paths[0]

    img = cv2.imread( str( path ), cv2.IMREAD_UNCHANGED )

    arr = img.reshape( (-1, 4) )

    cnts = Counter()
    cnts.update( tuple( pix ) for pix in arr )
    # %%


def _convert_to_puzzle( img: Array) -> Array:
    orig_shape = img.shape

    img2 = img.copy()
    sum_ = np.sum( img, axis=(2,) )
    non_transparent = (sum_ > 0 ).reshape( (orig_shape[0], orig_shape[1], 1))

    img2[:, :, 0:3] = 255 * (~non_transparent)

    return img2
    # %%
