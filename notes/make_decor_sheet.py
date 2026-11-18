import pathlib

from PIL import Image

out = pathlib.Path(r"E:\flutter\open-deepseek\figure\out")
notes = pathlib.Path(r"E:\flutter\open-deepseek\notes")

names = ["decor-ink", "decor-maid", "decor-tech", "decor-sumi", "decor-moon", "decor-gyu"]
cell = 340
sheet = Image.new("RGB", (cell * 3, cell * 2), "white")
for index, name in enumerate(names):
    art = Image.open(out / f"{name}.webp").convert("RGB").resize((cell, cell), Image.LANCZOS)
    sheet.paste(art, ((index % 3) * cell, (index // 3) * cell))
sheet.save(notes / "decor-sheet.jpg", "JPEG", quality=86)
print("sheet ok", sheet.size)
