
from collections import Counter
from pathlib import Path
from typing import List

import cv2
import numpy as np
from tangram.bin.common import PUZZLE_SUFFIX, PZLS_PATH, SOLS_PATH, SOLS_PATTERN, Array

# %%


def make_puzzles_from_solutions():
    # %%
    PZLS_PATH.mkdir(exist_ok=True, parents=True)
    sub_dirs = [elem for elem in list(SOLS_PATH.glob('*')) if elem.is_dir()]
    # %%

    for sub_dir in sub_dirs:
        dest_dir = PZLS_PATH / sub_dir.name
        # remove previously existing files
        for existing_file in dest_dir.glob('*'):
            existing_file.unlink()

        sol_paths = list(sub_dir.glob(SOLS_PATTERN))
        print(f'puzzle from solution for: {len(sol_paths):3d} @ {sub_dir.name}')
        for path in sol_paths:
            out_path = dest_dir / (path.stem + PUZZLE_SUFFIX)
            out_path.parent.mkdir(exist_ok=True)
            if out_path.exists():
                continue

            # print( path.stem )
            img = cv2.imread(str(path), cv2.IMREAD_UNCHANGED)

            img2 = _convert_to_puzzle(img)
            cv2.imwrite( str(out_path), img2 )

        assert len(sol_paths) == len(list(dest_dir.glob('*')))
    # %%


def _interactive_testing(paths: List[Path]):
    # %%
    path = paths[0]

    img = cv2.imread( str( path ), cv2.IMREAD_UNCHANGED )

    arr = img.reshape( (-1, 4) )

    cnts = Counter()
    cnts.update( tuple( pix ) for pix in arr )
    # %%


def _convert_to_puzzle(img: Array) -> Array:
    orig_shape = img.shape

    img2 = img.copy()
    sum_ = np.sum( img, axis=(2,) )
    non_transparent = (sum_ > 0 ).reshape( (orig_shape[0], orig_shape[1], 1))

    img2[:, :, 0:3] = 255 * (~non_transparent)

    return img2
    # %%
