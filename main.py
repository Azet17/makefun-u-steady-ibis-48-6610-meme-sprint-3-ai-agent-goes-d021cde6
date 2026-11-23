"""Copy the rogue-agent meme image to /output/entry.png.

Stdlib only. No network, no secrets, no reads outside this repo.
"""

import os
import shutil
import struct

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
DST = "/output/entry.png"
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1_048_576
MAX_DIM = 1024


def png_dimensions(path):
    """Read width/height from the PNG IHDR chunk (stdlib only)."""
    with open(path, "rb") as f:
        header = f.read(33)
    if len(header) < 33 or header[:8] != PNG_MAGIC:
        raise SystemExit("entry.png is not a PNG file")
    if header[12:16] != b"IHDR":
        raise SystemExit("entry.png has no IHDR chunk")
    width, height = struct.unpack(">II", header[16:24])
    return width, height


def main():
    width, height = png_dimensions(SRC)
    if width > MAX_DIM or height > MAX_DIM:
        raise SystemExit(
            f"entry.png is {width}x{height}, over the {MAX_DIM}x{MAX_DIM} cap"
        )

    size = os.path.getsize(SRC)
    if size > MAX_BYTES:
        raise SystemExit(f"entry.png is {size} bytes, over the 1 MiB cap")

    os.makedirs("/output", exist_ok=True)
    shutil.copyfile(SRC, DST)

    out_size = os.path.getsize(DST)
    out_w, out_h = png_dimensions(DST)
    print(f"entry.png: {width}x{height}, {size} bytes")
    print(f"wrote {DST}: {out_w}x{out_h}, {out_size} bytes")


if __name__ == "__main__":
    main()
