"""dl_all.py가 받은 raw*.bin -> topics/<id>/images/figNN.(jpg|png) 변환 + <tag>_meta.json 생성.
사용: python make_images.py <작업폴더> <tag> <topic-id>
규칙: EXIF 회전 적용, 1500KB 초과 또는 폭 1500px 초과면 폭 1400px JPEG(q82), 아니면 PNG(원본 유지).
meta 형식: [[파일명, 폭, 높이, 바이트], ...]  (Builder가 <img width height>에 사용)
"""
import sys, os, io, json, glob
from PIL import Image, ImageOps
SP = sys.argv[1].rstrip("/\\") + "/"; tag, pid = sys.argv[2], sys.argv[3]
PROJ = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "topics")).replace("\\", "/") + "/"
out = PROJ + pid + "/images/"; os.makedirs(out, exist_ok=True)
meta = []
for i, f in enumerate(sorted(glob.glob(SP + tag + "/raw*.bin")), 1):
    raw = open(f, "rb").read()
    im = ImageOps.exif_transpose(Image.open(io.BytesIO(raw)))
    big = len(raw) > 1500 * 1024 or im.width > 1500
    if big:
        if im.width > 1400:
            im = im.resize((1400, round(im.height * 1400 / im.width)), Image.LANCZOS)
        fn = f"fig{i:02d}.jpg"; im.convert("RGB").save(out + fn, "JPEG", quality=82, optimize=True)
    else:
        fn = f"fig{i:02d}.png"; im.save(out + fn, "PNG", optimize=True)
    meta.append([fn, im.width, im.height, os.path.getsize(out + fn)])
json.dump(meta, open(SP + f"{tag}_meta.json", "w"))
print("images:", len(meta), "MB:", round(sum(m[3] for m in meta) / 1e6, 1))
