"""Make full-frame responsive WebP assets from the supplied phase 3 photos.

Requires Pillow for maintenance only; hosting has no Python dependency.
Original photographs are never overwritten or cropped.
"""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
PHOTOS = [
    ("a cup for your kind of day.jpeg", "phase3-coffee", "Coffee & drinks preview", (480, 960)),
    ("pull up a chair.jpeg", "phase3-breakfast", "All-day breakfast category preview", (480, 960)),
    ("save room for something sweet.jpg", "phase3-croissant", "Croissant category preview", (480, 960)),
    ("a little more  than a coffee.jpg", "phase3-table", "A Closer Look: shared table and lamp", (480, 960, 1152)),
]


def record(path, image):
    return {"file": path.relative_to(ROOT).as_posix(), "width": image.width,
            "height": image.height, "bytes": path.stat().st_size,
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


manifest = {"reviewed": "2026-10-04", "method": "EXIF orientation, RGB, full-frame proportional LANCZOS resize, WebP quality 85 / method 6",
            "identification": "Broad visible categories only. Exact dish/drink names and ingredients unverified; see Docs/PHASE-3-PHOTOS.md.", "photos": []}
for filename, stem, use, widths in PHOTOS:
    source = ROOT / "images" / "menu" / "phase 3" / filename
    with Image.open(source) as original:
        image = ImageOps.exif_transpose(original).convert("RGB")
        entry = {"source": record(source, image), "use": use, "variants": []}
        for width in widths:
            width = min(width, image.width)
            resized = image.resize((width, round(image.height * width / image.width)), Image.Resampling.LANCZOS)
            output = ROOT / "dist" / "assets" / f"{stem}-{width}.webp"
            resized.save(output, "WEBP", quality=85, method=6)
            entry["variants"].append(record(output, resized))
            print(f"{output.name}: {resized.width}x{resized.height}, {output.stat().st_size} bytes")
        manifest["photos"].append(entry)
(ROOT / "Docs" / "evidence" / "phase3-assets.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
