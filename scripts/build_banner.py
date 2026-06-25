from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets" / "banner-source.png"
OUTPUT = ROOT / "assets" / "banner.png"

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


source = Image.open(SOURCE).convert("RGB")
source_ratio = source.width / source.height
target_ratio = WIDTH / HEIGHT

if source_ratio > target_ratio:
    crop_width = round(source.height * target_ratio)
    left = (source.width - crop_width) // 2
    source = source.crop((left, 0, left + crop_width, source.height))
else:
    crop_height = round(source.width / target_ratio)
    top = (source.height - crop_height) // 2
    source = source.crop((0, top, source.width, top + crop_height))

canvas = source.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS).convert("RGBA")

# Deepen the left-side text field without obscuring the generated data scene.
shade = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
shade_draw = ImageDraw.Draw(shade)
for x in range(0, 1480):
    opacity = int(150 * (1 - (x / 1480)) ** 1.35)
    shade_draw.line((x, 0, x, HEIGHT), fill=(2, 6, 16, opacity))
canvas.alpha_composite(shade)

# Restrained ambient glows.
glow = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
glow_draw = ImageDraw.Draw(glow)
glow_draw.ellipse((-260, 970, 520, 1750), fill=(42, 104, 255, 75))
glow_draw.ellipse((630, -420, 1430, 380), fill=(113, 66, 255, 42))
glow = glow.filter(ImageFilter.GaussianBlur(115))
canvas.alpha_composite(glow)

rounded_panel(
    canvas,
    (110, 218, 1195, 1205),
    radius=40,
    fill=(7, 13, 29, 165),
    outline=(91, 139, 255, 95),
)

draw = ImageDraw.Draw(canvas)

# Monogram and small profile descriptor.
draw.rounded_rectangle((178, 292, 290, 404), radius=28, fill=(22, 72, 188, 175), outline=(119, 162, 255, 190), width=2)
draw.text((211, 313), "MS", font=font(FONT_SEMIBOLD, 42), fill=(242, 247, 255, 255))
draw.text(
    (326, 305),
    "DATA  /  CLOUD  /  ENGINEERING",
    font=font(FONT_SEMIBOLD, 27),
    fill=(138, 170, 255, 255),
)
draw.text(
    (326, 350),
    "INDIA  ·  MCA 2025–2027",
    font=font(FONT_REGULAR, 25),
    fill=(160, 172, 200, 255),
)

# Main identity.
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
        fill=(12, 27, 58, 220),
        outline=(74, 119, 220, 170),
        width=2,
    )
    draw.text((cursor_x + 24, 1035), skill, font=skill_font, fill=(204, 218, 250, 255))
    cursor_x += chip_width + 16

# Subtle edge treatment for GitHub's dark canvas.
draw.rounded_rectangle((4, 4, WIDTH - 5, HEIGHT - 5), radius=28, outline=(61, 96, 174, 115), width=4)

canvas.convert("RGB").save(OUTPUT, "PNG", optimize=True)
print(f"Created {OUTPUT} ({WIDTH}x{HEIGHT})")
