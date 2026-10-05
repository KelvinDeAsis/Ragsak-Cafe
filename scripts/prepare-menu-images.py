"""Create complete WebP menu photos without cropping or removing attribution."""
from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
for source, output in [
    ("all day breakfast.jpg", "breakfast-menu.webp"),
    ("drinks.jpg", "drinks-menu.webp"),
]:
    with Image.open(ROOT / "images" / "menu" / source) as photo:
        image = ImageOps.exif_transpose(photo).convert("RGB")
        destination = ROOT / "dist" / "assets" / output
        image.save(destination, "WEBP", quality=92, method=6)
        print(f"{source}: {image.width}x{image.height} -> {output} ({destination.stat().st_size} bytes)")
