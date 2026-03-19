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

    # Add top highlight and lower vignette to match the glossy tile feeling.
    gdraw.ellipse((120, 40, 940, 640), fill=(255, 255, 255, 42))
    gdraw.ellipse((120, 520, 940, 1080), fill=(0, 120, 80, 35))
    img.paste(gradient, (0, 0), mask)

    # Add subtle blueprint grid lines on top of the gradient background.
    grid = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
    g = ImageDraw.Draw(grid)
    step = 96
    for x in range(pad + 8, 1024 - pad, step):
        g.line((x, pad + 8, x, 1024 - pad - 8), fill=(210, 245, 220, 60), width=2)
    for y in range(pad + 8, 1024 - pad, step):
        g.line((pad + 8, y, 1024 - pad - 8, y), fill=(210, 245, 220, 60), width=2)
    img.alpha_composite(grid)

    # Add soft circular construction rings as in the reference icon.
    rings = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
    r = ImageDraw.Draw(rings)
    cx = cy = 512
    for radius in [340, 245, 145]:
        r.ellipse((cx - radius, cy - radius, cx + radius, cy + radius), outline=(220, 248, 228, 72), width=4)
    img.alpha_composite(rings)

    # Add a thin bright border for the rounded-square tile edge.
    border = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
    b = ImageDraw.Draw(border)
    b.rounded_rectangle((pad + 2, pad + 2, 1024 - pad - 2, 1024 - pad - 2), radius=188, outline=(235, 255, 235, 95), width=4)
    b.rounded_rectangle((pad, pad, 1024 - pad, 1024 - pad), radius=190, outline=(35, 140, 90, 90), width=3)
    img.alpha_composite(border)

    # Draw a beveled white E with soft drop shadow to match the exact style request.
    ex = 292
    ey = 246
    ew = 430
    eh = 528
    et = 98

    # Shadow layer behind the E.
    shadow = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
    s = ImageDraw.Draw(shadow)
    ox = 10
    oy = 14
    s.rectangle((ex + ox, ey + oy, ex + et + ox, ey + eh + oy), fill=(0, 0, 0, 55))
    s.rectangle((ex + ox, ey + oy, ex + ew + ox, ey + et + oy), fill=(0, 0, 0, 55))
    s.rectangle((ex + ox, ey + eh // 2 - et // 2 + oy, ex + ew - 86 + ox, ey + eh // 2 + et // 2 + oy), fill=(0, 0, 0, 55))
    s.rectangle((ex + ox, ey + eh - et + oy, ex + ew + ox, ey + eh + oy), fill=(0, 0, 0, 55))
    img.alpha_composite(shadow)

    # Front face of the E.
    draw.rectangle((ex, ey, ex + et, ey + eh), fill=(246, 249, 242, 255))
    draw.rectangle((ex, ey, ex + ew, ey + et), fill=(246, 249, 242, 255))
    draw.rectangle((ex, ey + eh // 2 - et // 2, ex + ew - 86, ey + eh // 2 + et // 2), fill=(246, 249, 242, 255))
    draw.rectangle((ex, ey + eh - et, ex + ew, ey + eh), fill=(246, 249, 242, 255))

    # Bevel / edge shading for depth.
    draw.line((ex, ey + eh, ex + ew, ey + eh), fill=(182, 191, 174, 255), width=5)
    draw.line((ex + ew, ey, ex + ew, ey + et), fill=(182, 191, 174, 255), width=5)
    draw.line((ex + ew - 86, ey + eh // 2 + et // 2, ex + ew - 86, ey + eh // 2 - et // 2), fill=(182, 191, 174, 255), width=4)

    # Top-left soft highlight line on E for embossed look.
    draw.line((ex + 6, ey + 6, ex + ew - 8, ey + 6), fill=(255, 255, 255, 180), width=4)
    draw.line((ex + 6, ey + 6, ex + 6, ey + eh - 8), fill=(255, 255, 255, 160), width=4)

    # Gentle center glow behind E to increase contrast.
    halo = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
    hdraw = ImageDraw.Draw(halo)
    hdraw.ellipse((250, 230, 790, 800), fill=(255, 255, 255, 35))
    img.alpha_composite(halo)
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
