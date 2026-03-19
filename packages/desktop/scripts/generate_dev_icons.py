import subprocess
from pathlib import Path

from PIL import Image, ImageDraw


# Regenerates desktop icon assets with a green OpenEcon E mark.
ROOT = Path(__file__).resolve().parents[1] / "src-tauri" / "icons"


def make_base() -> Image.Image:
    img = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Build rounded-square mask first so every effect is clipped to icon shape.
    pad = 80
    mask = Image.new("L", (1024, 1024), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle((pad, pad, 1024 - pad, 1024 - pad), radius=190, fill=255)

    # Build vertical green gradient close to the provided reference.
    gradient = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(gradient)
    top = (164, 230, 102, 255)
    bottom = (20, 182, 101, 255)
    for y in range(1024):
        ratio = y / 1023
        color = (
            int(top[0] * (1 - ratio) + bottom[0] * ratio),
            int(top[1] * (1 - ratio) + bottom[1] * ratio),
            int(top[2] * (1 - ratio) + bottom[2] * ratio),
            255,
        )
        gdraw.line((0, y, 1024, y), fill=color)

    # No sheen - keep clean gradient.
    img.paste(gradient, (0, 0), mask)

    # Add subtle blueprint grid lines on top of the gradient background.
    grid = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
    g = ImageDraw.Draw(grid)
    step = 96
    for x in range(pad + 8, 1024 - pad, step):
        g.line((x, pad + 8, x, 1024 - pad - 8), fill=(210, 245, 220, 25), width=1)
    for y in range(pad + 8, 1024 - pad, step):
        g.line((pad + 8, y, 1024 - pad - 8, y), fill=(210, 245, 220, 25), width=1)
    img.alpha_composite(grid)

    # Add soft circular construction rings as in the reference icon.
    rings = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
    r = ImageDraw.Draw(rings)
    cx = cy = 512
    for radius in [340, 245, 145]:
        r.ellipse((cx - radius, cy - radius, cx + radius, cy + radius), outline=(220, 248, 228, 28), width=2)
    img.alpha_composite(rings)

    # Add a thin bright border for the rounded-square tile edge.
    border = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
    b = ImageDraw.Draw(border)
    b.rounded_rectangle((pad + 2, pad + 2, 1024 - pad - 2, 1024 - pad - 2), radius=188, outline=(235, 255, 235, 95), width=4)
    b.rounded_rectangle((pad, pad, 1024 - pad, 1024 - pad), radius=190, outline=(35, 140, 90, 90), width=3)
    img.alpha_composite(border)

    # Draw a 3D extruded white E matching the reference icon.
    # E fits comfortably inside the rounded-square with good margins.
    ex = 300          # left edge x
    ey = 260          # top edge y
    ew = 420          # total width of the E
    eh = 510          # total height of the E
    et = 100          # stroke thickness
    mid_w = ew - 80   # middle bar is shorter

    # Depth / extrusion offset (bottom-right direction).
    dx = 14
    dy = 16
    depth_color = (20, 90, 45, 180)  # dark green for 3D depth

    # Define the four rects that make up the E (left bar, top bar, mid bar, bottom bar).
    bars_front = [
        (ex, ey, ex + et, ey + eh),                               # left vertical
        (ex, ey, ex + ew, ey + et),                                # top horizontal
        (ex + et, ey + eh // 2 - et // 2, ex + mid_w, ey + eh // 2 + et // 2),  # middle
        (ex, ey + eh - et, ex + ew, ey + eh),                     # bottom horizontal
    ]

    # Draw the 3D extrusion layer first (offset copy in depth_color).
    extrusion = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
    ed = ImageDraw.Draw(extrusion)
    for x1, y1, x2, y2 in bars_front:
        ed.rectangle((x1 + dx, y1 + dy, x2 + dx, y2 + dy), fill=depth_color)
    img.alpha_composite(extrusion)

    # Front face of the E (white).
    face_color = (250, 253, 248, 255)
    for x1, y1, x2, y2 in bars_front:
        draw.rectangle((x1, y1, x2, y2), fill=face_color)

    # Subtle bottom/right bevel on front face for depth.
    bevel = (210, 218, 204, 255)
    draw.line((ex, ey + eh, ex + ew, ey + eh), fill=bevel, width=3)
    draw.line((ex + ew, ey, ex + ew, ey + et), fill=bevel, width=3)
    draw.line((ex + ew, ey + eh - et, ex + ew, ey + eh), fill=bevel, width=3)
    draw.line((ex + mid_w, ey + eh // 2 - et // 2, ex + mid_w, ey + eh // 2 + et // 2), fill=bevel, width=3)

    # Top-left highlight on E for embossed look.
    draw.line((ex + 3, ey + 3, ex + ew - 3, ey + 3), fill=(255, 255, 255, 180), width=3)
    draw.line((ex + 3, ey + 3, ex + 3, ey + eh - 3), fill=(255, 255, 255, 150), width=3)
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

    # Convert iconset to .icns using macOS iconutil.
    icns_path = target / "icon.icns"
    subprocess.run(["iconutil", "--convert", "icns", str(iconset), "--output", str(icns_path)], check=True)


base = make_base()
# Also write to root icons directory because Tauri dev runtime may read default
# icon paths (icons/icon.icns, icons/32x32.png, etc.) instead of channel folders.
write_set(ROOT, base)
print(str(ROOT))

for channel in ["dev", "prod", "beta"]:
    write_set(ROOT / channel, base)
    print(str(ROOT / channel))
