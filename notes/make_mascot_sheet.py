import pathlib

from PIL import Image

out = pathlib.Path(r"E:\flutter\open-deepseek\figure\out")
notes = pathlib.Path(r"E:\flutter\open-deepseek\notes")

names = ["mascot-ink", "mascot-plain", "mascot-sumi", "mascot-moon", "mascot-gyu"]
cell_w, cell_h = 300, 420
sheet = Image.new("RGB", (cell_w * 5, cell_h), "white")
for index, name in enumerate(names):
    art = Image.open(out / f"{name}.png").convert("RGB")
    art.thumbnail((cell_w, cell_h), Image.LANCZOS)
    sheet.paste(art, (index * cell_w + (cell_w - art.width) // 2, (cell_h - art.height) // 2))
sheet.save(notes / "mascot-sheet.jpg", "JPEG", quality=88)
print("sheet ok", sheet.size)
