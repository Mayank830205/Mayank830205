from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets" / "banner-source.png"
PORTRAIT = ROOT / "assets" / "mayank-github-profile.png"
OUTPUT = ROOT / "assets" / "banner-v2.png"

WIDTH, HEIGHT = 2560, 1440
FONT_REGULAR = Path(r"C:\Windows\Fonts\segoeui.ttf")
FONT_SEMIBOLD = Path(r"C:\Windows\Fonts\segoeuib.ttf")


def font(path: Path, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(path), size)


def rounded_panel(
    canvas: Image.Image,
    box: tuple[int, int, int, int],
    radius: int,
    fill: tuple[int, int, int, int],
    outline: tuple[int, int, int, int],
) -> None:
    panel = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(panel)
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=2)
    canvas.alpha_composite(panel)


def rounded_image(
    image: Image.Image,
    size: tuple[int, int],
    radius: int,
    centering: tuple[float, float] = (0.5, 0.5),
) -> Image.Image:
    fitted = ImageOps.fit(
        image.convert("RGB"),
        size,
        method=Image.Resampling.LANCZOS,
        centering=centering,
    ).convert("RGBA")
    mask = Image.new("L", size, 0)
    ImageDraw.Draw(mask).rounded_rectangle(
        (0, 0, size[0] - 1, size[1] - 1),
        radius=radius,
        fill=255,
    )
    fitted.putalpha(mask)
    return fitted


source = Image.open(SOURCE).convert("RGB")
source = ImageOps.fit(source, (WIDTH, HEIGHT), method=Image.Resampling.LANCZOS)
canvas = source.convert("RGBA")

# Deepen the left text field while keeping the right-side data scene visible.
shade = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
shade_draw = ImageDraw.Draw(shade)
for x in range(0, 1500):
    opacity = int(160 * (1 - (x / 1500)) ** 1.3)
    shade_draw.line((x, 0, x, HEIGHT), fill=(2, 6, 16, opacity))
canvas.alpha_composite(shade)

# Ambient lighting.
glow = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
glow_draw = ImageDraw.Draw(glow)
glow_draw.ellipse((-260, 970, 520, 1750), fill=(42, 104, 255, 75))
glow_draw.ellipse((630, -420, 1430, 380), fill=(113, 66, 255, 42))
glow = glow.filter(ImageFilter.GaussianBlur(115))
canvas.alpha_composite(glow)

# Identity panel.
rounded_panel(
    canvas,
    (110, 218, 1195, 1205),
    radius=40,
    fill=(7, 13, 29, 172),
    outline=(91, 139, 255, 105),
)

draw = ImageDraw.Draw(canvas)
draw.rounded_rectangle(
    (178, 292, 290, 404),
    radius=28,
    fill=(22, 72, 188, 185),
    outline=(119, 162, 255, 200),
    width=2,
)
draw.text((211, 313), "MS", font=font(FONT_SEMIBOLD, 42), fill=(242, 247, 255, 255))
draw.text(
    (326, 305),
    "DATA  /  CLOUD  /  ENGINEERING",
    font=font(FONT_SEMIBOLD, 27),
    fill=(138, 170, 255, 255),
)
draw.text(
    (326, 350),
    "INDIA  /  MCA 2025-2027",
    font=font(FONT_REGULAR, 25),
    fill=(160, 172, 200, 255),
)

draw.text((178, 494), "MAYANK", font=font(FONT_SEMIBOLD, 112), fill=(247, 249, 255, 255))
draw.text((178, 615), "SHRINGI", font=font(FONT_SEMIBOLD, 112), fill=(107, 149, 255, 255))
draw.rounded_rectangle((180, 766, 895, 770), radius=2, fill=(83, 132, 255, 225))
draw.ellipse((895, 758, 919, 782), fill=(139, 94, 255, 255))
draw.text(
    (178, 822),
    "Aspiring Data Analyst  |  Data Engineer",
    font=font(FONT_SEMIBOLD, 43),
    fill=(224, 232, 249, 255),
)
draw.text(
    (178, 897),
    "Turning Data Into Decisions",
    font=font(FONT_REGULAR, 41),
    fill=(170, 184, 214, 255),
)

skills = ["PYTHON", "SQL", "AWS", "POWER BI", "ETL"]
cursor_x = 178
for skill in skills:
    skill_font = font(FONT_SEMIBOLD, 23)
    bbox = draw.textbbox((0, 0), skill, font=skill_font)
    chip_width = bbox[2] - bbox[0] + 48
    draw.rounded_rectangle(
        (cursor_x, 1018, cursor_x + chip_width, 1082),
        radius=20,
        fill=(12, 27, 58, 225),
        outline=(74, 119, 220, 175),
        width=2,
    )
    draw.text((cursor_x + 24, 1035), skill, font=skill_font, fill=(204, 218, 250, 255))
    cursor_x += chip_width + 16

# Portrait card.
portrait_glow = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
portrait_glow_draw = ImageDraw.Draw(portrait_glow)
portrait_glow_draw.rounded_rectangle(
    (1640, 176, 2432, 1255),
    radius=86,
    fill=(54, 111, 255, 92),
)
portrait_glow = portrait_glow.filter(ImageFilter.GaussianBlur(78))
canvas.alpha_composite(portrait_glow)

rounded_panel(
    canvas,
    (1662, 192, 2410, 1236),
    radius=58,
    fill=(6, 12, 27, 195),
    outline=(115, 153, 255, 165),
)

portrait = rounded_image(
    Image.open(PORTRAIT),
    size=(690, 900),
    radius=42,
    centering=(0.5, 0.40),
)
canvas.alpha_composite(portrait, (1691, 221))

portrait_fade = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
portrait_fade_draw = ImageDraw.Draw(portrait_fade)
for y in range(930, 1122):
    opacity = int(205 * ((y - 930) / 192) ** 1.5)
    portrait_fade_draw.line((1691, y, 2380, y), fill=(5, 10, 24, opacity))
canvas.alpha_composite(portrait_fade)

draw = ImageDraw.Draw(canvas)
draw.rounded_rectangle(
    (1775, 1084, 2296, 1152),
    radius=24,
    fill=(10, 24, 52, 235),
    outline=(84, 132, 244, 185),
    width=2,
)
draw.ellipse((1800, 1107, 1818, 1125), fill=(82, 208, 137, 255))
draw.text(
    (1835, 1102),
    "OPEN TO OPPORTUNITIES",
    font=font(FONT_SEMIBOLD, 24),
    fill=(220, 231, 255, 255),
)

draw.rounded_rectangle(
    (4, 4, WIDTH - 5, HEIGHT - 5),
    radius=28,
    outline=(61, 96, 174, 120),
    width=4,
)

canvas.convert("RGB").save(OUTPUT, "PNG", optimize=True)
print(f"Created {OUTPUT} ({WIDTH}x{HEIGHT})")
