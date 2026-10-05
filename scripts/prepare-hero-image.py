"""Optimize the user-selected hero photo without changing its contents."""
from pathlib import Path
from PIL import Image, ImageOps

root = Path(__file__).resolve().parent.parent
source = root / "images" / "menu" / "ragsak bg.jpg"
with Image.open(source) as original:
    image = ImageOps.exif_transpose(original).convert("RGB")
    print(f"Source: {image.width}x{image.height}")
    for width in (640, 960, 1536):
        height = round(image.height * width / image.width)
        output = root / "dist" / "assets" / f"hero-sign-{width}.webp"
        image.resize((width, height), Image.Resampling.LANCZOS).save(output, "WEBP", quality=86, method=6)
        print(f"{output.name}: {width}x{height}, {output.stat().st_size} bytes")
