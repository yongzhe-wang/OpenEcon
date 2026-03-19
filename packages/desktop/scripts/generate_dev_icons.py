from pathlib import Path

from PIL import Image, ImageDraw


# Regenerates desktop icon assets with a green OpenEcon E mark.
ROOT = Path(__file__).resolve().parents[1] / "src-tauri" / "icons"


def make_base() -> Image.Image:
    img = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Green rounded-square background.
    pad = 80
    draw.rounded_rectangle((pad, pad, 1024 - pad, 1024 - pad), radius=220, fill=(22, 163, 74, 255))

    # White block-style letter E.
    x = 320
    y = 250
    w = 380
    h = 520
    th = 90
    draw.rectangle((x, y, x + th, y + h), fill=(255, 255, 255, 255))
    draw.rectangle((x, y, x + w, y + th), fill=(255, 255, 255, 255))
    draw.rectangle((x, y + h // 2 - th // 2, x + w - 90, y + h // 2 + th // 2), fill=(255, 255, 255, 255))
    draw.rectangle((x, y + h - th, x + w, y + h), fill=(255, 255, 255, 255))
    return img


def write_set(target: Path, img: Image.Image):
    target.mkdir(parents=True, exist_ok=True)

    # Export all pngs consumed by Tauri + platform packaging.
    sizes = {
        "32x32.png": 32,
        "64x64.png": 64,
        "128x128.png": 128,
        "128x128@2x.png": 256,
        "icon.png": 512,
        "Square30x30Logo.png": 30,
        "Square44x44Logo.png": 44,
        "Square71x71Logo.png": 71,
        "Square89x89Logo.png": 89,
        "Square107x107Logo.png": 107,
        "Square142x142Logo.png": 142,
        "Square150x150Logo.png": 150,
        "Square284x284Logo.png": 284,
        "Square310x310Logo.png": 310,
        "StoreLogo.png": 50,
    }
    for name, size in sizes.items():
        img.resize((size, size), Image.Resampling.LANCZOS).save(target / name)

    # Build Windows icon.
    img.resize((256, 256), Image.Resampling.LANCZOS).save(
        target / "icon.ico",
        format="ICO",
        sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)],
    )

    # Build macOS iconset source files (converted to .icns by iconutil).
    iconset = target / "icon.iconset"
    iconset.mkdir(exist_ok=True)
    for size in [16, 32, 128, 256, 512]:
        img.resize((size, size), Image.Resampling.LANCZOS).save(iconset / f"icon_{size}x{size}.png")
        img.resize((size * 2, size * 2), Image.Resampling.LANCZOS).save(iconset / f"icon_{size}x{size}@2x.png")


base = make_base()
for channel in ["dev", "prod", "beta"]:
    write_set(ROOT / channel, base)
    print(str(ROOT / channel))
