#!/usr/bin/env python3
"""news-23-b12-numbers-led: copy the bundled entry image to the output dir.

Stdlib only. Reads entry.png next to this file, verifies its PNG header
(1024x1024), copies it to $MAKEFUN_OUTPUT_DIR/entry.png (default: out/),
then verifies the destination byte-for-byte. Never writes next to main.py.
"""
import hashlib
import os
import shutil
import struct
import sys

EXPECTED_W, EXPECTED_H = 1024, 1024


def png_size(path):
    with open(path, "rb") as f:
        head = f.read(33)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        raise SystemExit("not a PNG file: %s" % path)
    if head[12:16] != b"IHDR":
        raise SystemExit("missing IHDR chunk: %s" % path)
    w, h = struct.unpack(">II", head[16:24])
    return w, h


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    w, h = png_size(src)
    if (w, h) != (EXPECTED_W, EXPECTED_H):
        raise SystemExit("entry.png is %dx%d, expected 1024x1024" % (w, h))
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    s1, s2 = sha256(src), sha256(dst)
    if s1 != s2:
        raise SystemExit("copy mismatch: %s != %s" % (s1, s2))
    dw, dh = png_size(dst)
    if (dw, dh) != (EXPECTED_W, EXPECTED_H):
        raise SystemExit("destination is %dx%d, expected 1024x1024" % (dw, dh))
    print("OK entry.png %dx%d sha256=%s bytes=%d"
          % (w, h, s2, os.path.getsize(dst)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
