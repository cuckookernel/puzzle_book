
from typing import List
from pathlib import Path
from collections import Counter
import numpy as np

import cv2

from tangram.bin.common import SOLS_PATH, SOLS_PATTERN, PZLS_PATH, PUZZLE_SUFFIX

Array = np.ndarray
# %%


def run():
    # %%
    PZLS_PATH.mkdir(exist_ok=True, parents=True)
    sub_dirs = [elem for elem in list(SOLS_PATH.glob('*')) if elem.is_dir()]
    # %%

    for sub_dir in sub_dirs:
        for path in sub_dir.glob(SOLS_PATTERN):
            out_path = PZLS_PATH / sub_dir.name / (path.stem + PUZZLE_SUFFIX)
            out_path.parent.mkdir(exist_ok=True)
            if out_path.exists():
                continue

            print( path.stem )
            img = cv2.imread( str( path ), cv2.IMREAD_UNCHANGED )

            img2 = _convert_to_puzzle(img)
            cv2.imwrite( str(out_path), img2 )
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
