
from importlib import reload
from pathlib import Path

import cv2
import tangram.bin.common as com
from tangram.bin.common import SOLS_PATH

SOURCE_DIR = SOLS_PATH.parent / "white-background"
TARGET_DIR = SOLS_PATH / 'wbg-transformed'
# %%


def _interactive_testing():
    # %%
    wbg_paths = list(SOURCE_DIR.glob('*'))

    img_path = wbg_paths[0]
    print(img_path)
    # %%
    reload(com)
    for img_path in wbg_paths:
        do_one(img_path)
    # %%


def do_one(img_path: Path):
    img = cv2.imread( str(img_path), cv2.IMREAD_UNCHANGED )

    img2 = wbg_to_transparent(img)
    target_path = com.make_target_path(img_path, TARGET_DIR, add_hash=True)
    print(target_path)
    cv2.imwrite( str(target_path), img2 )


def wbg_to_transparent(img):
    white_bg = img.sum(axis=2) == 1020  # 255 * 4  pixel is white
    img2 = img.copy()
    img2[:, :, 3] = img[:, :, 3] * (~white_bg)
    return img2
