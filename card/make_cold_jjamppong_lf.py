import json
from pathlib import Path

import make_lr_lf_cards as cardmaker
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "summer-food-2026" / "lf-data.json"
ASSETS = ROOT / "summer-food-2026" / "assets"
OUT = ROOT / "lf-card"
CONTACT_SHEET = ROOT / "compare-card" / "summer_lf_021_040_contact_sheet.jpg"


def main():
    items = json.loads(DATA.read_text(encoding="utf-8"))
    OUT.mkdir(parents=True, exist_ok=True)
    rendered = []
    for item in items:
        item["hero_path"] = str(ASSETS / f"{item['id']}_{item['code']}_hero.png")
        cardmaker.PRONUNCIATION[item["id"]] = item.pop("pron")
        card = cardmaker.make_fine_dining_en(item)
        path = OUT / f"{item['id']}_{item['code']}_lf.png"
        card.save(path, quality=95)
        rendered.append((item, card))
        print(path)

    thumb_w, thumb_h = 300, 329
    label_h = 42
    sheet = Image.new("RGB", (thumb_w * 5, (thumb_h + label_h) * 4), (242, 238, 247))
    draw = ImageDraw.Draw(sheet)
    label_font = ImageFont.truetype(cardmaker.FONT_BOLD, 20)
    for index, (item, card) in enumerate(rendered):
        col, row = index % 5, index // 5
        thumb = card.copy()
        thumb.thumbnail((thumb_w, thumb_h), Image.Resampling.LANCZOS)
        x = col * thumb_w + (thumb_w - thumb.width) // 2
        y = row * (thumb_h + label_h)
        sheet.paste(thumb, (x, y))
        draw.text((col * thumb_w + 12, y + thumb_h + 8), f"{item['id']}  {item['en']}", font=label_font, fill=(72, 36, 128))
    CONTACT_SHEET.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(CONTACT_SHEET, quality=92)
    print(CONTACT_SHEET)


if __name__ == "__main__":
    main()
