from pathlib import Path
from urllib.parse import quote

import qrcode
from PIL import Image, ImageDraw, ImageFont, ImageOps


ROOT = Path(r"C:\Discovery\Cosmo\dev\lab\utility\card")
SOURCE = Path(r"C:\Discovery\Cosmo\dev\maker-and-made\data\images\lm\001_kmj.png")
OUT = ROOT / "output"

W, H = 1198, 1313
FONT_REG = r"C:\Windows\Fonts\malgun.ttf"
FONT_BOLD = r"C:\Windows\Fonts\malgunbd.ttf"


def font(size, bold=False):
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REG, size)


def rounded(im, radius):
    mask = Image.new("L", im.size, 0)
    d = ImageDraw.Draw(mask)
    d.rounded_rectangle((0, 0, im.size[0] - 1, im.size[1] - 1), radius=radius, fill=255)
    out = Image.new("RGBA", im.size, (0, 0, 0, 0))
    out.paste(im.convert("RGBA"), (0, 0), mask)
    return out


def fit_crop(im, size):
    return ImageOps.fit(im.convert("RGB"), size, method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))


def text(draw, xy, s, size, fill, bold=False, anchor=None, align="left"):
    draw.text(xy, s, font=font(size, bold), fill=fill, anchor=anchor, align=align)


def wrap(draw, s, max_w, size, bold=False):
    f = font(size, bold)
    lines = []
    for para in s.split("\n"):
        if " " in para:
            line = ""
            for word in para.split(" "):
                test = word if not line else line + " " + word
                if draw.textlength(test, font=f) <= max_w:
                    line = test
                else:
                    if line:
                        lines.append(line)
                    if draw.textlength(word, font=f) <= max_w:
                        line = word
                    else:
                        chunk = ""
                        for ch in word:
                            test_chunk = chunk + ch
                            if draw.textlength(test_chunk, font=f) <= max_w:
                                chunk = test_chunk
                            else:
                                if chunk:
                                    lines.append(chunk)
                                chunk = ch
                        line = chunk
            if line:
                lines.append(line)
            continue
        line = ""
        for ch in para:
            test = line + ch
            if draw.textlength(test, font=f) <= max_w:
                line = test
            else:
                if line:
                    lines.append(line)
                line = ch
        if line:
            lines.append(line)
    return lines


def multiline(draw, xy, s, max_w, size, fill, bold=False, line_gap=8):
    x, y = xy
    f = font(size, bold)
    for line in wrap(draw, s, max_w, size, bold):
        draw.text((x, y), line, font=f, fill=fill)
        y += size + line_gap
    return y


def card_base(accent, dark):
    im = Image.new("RGB", (W, H), (255, 250, 241))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((8, 8, W - 9, H - 9), radius=38, outline=dark, width=7)
    d.rounded_rectangle((30, 30, W - 30, 122), radius=32, fill=accent)
    return im, d


def chip(draw, xy, label, color, text_color=(255, 255, 255), w=None):
    x, y = xy
    f = font(25, True)
    tw = int(draw.textlength(label, font=f))
    width = w or tw + 36
    draw.rounded_rectangle((x, y, x + width, y + 46), radius=22, fill=color)
    draw.text((x + width / 2, y + 23), label, font=f, fill=text_color, anchor="mm")
    return x + width + 12


def chip_small(draw, xy, label, color, text_color=(255, 255, 255), w=None):
    x, y = xy
    f = font(22, True)
    tw = int(draw.textlength(label, font=f))
    width = w or tw + 30
    draw.rounded_rectangle((x, y, x + width, y + 40), radius=20, fill=color)
    draw.text((x + width / 2, y + 20), label, font=f, fill=text_color, anchor="mm")
    return x + width + 10


def qr_image(url, size=210, color=(0, 0, 0)):
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=8, border=2)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color=color, back_color="white").convert("RGB")
    return img.resize((size, size), Image.Resampling.NEAREST)


def source_food_crop():
    src = Image.open(SOURCE).convert("RGB")
    return src.crop((28, 350, 552, 858))


def source_bot_crop():
    src = Image.open(SOURCE).convert("RGB")
    return src.crop((575, 300, 1010, 820))


def make_lm_en():
    green = (0, 112, 88)
    deep = (0, 82, 66)
    ink = (22, 32, 30)
    im, d = card_base(green, deep)

    text(d, (58, 51), "MaAM LUNCH MENU", 29, (234, 255, 248), True)
    text(d, (58, 82), "LM TYPE · FOOD CHARACTER RESULT", 21, (210, 242, 232), False)
    text(d, (W - 58, 76), "KMJ-LM", 48, (255, 255, 255), True, anchor="rm")

    food = rounded(fit_crop(source_food_crop(), (500, 360)), 28)
    im.paste(food, (48, 158), food)
    d.rounded_rectangle((48, 158, 548, 518), radius=28, outline=(70, 153, 128), width=4)

    text(d, (590, 158), "KIMCHI JJIGAE", 56, ink, True)
    text(d, (594, 222), "김치찌개", 34, green, True)
    text(d, (594, 266), "FERMENTED KOREAN STEW", 24, green, False)
    multiline(
        d,
        (594, 318),
        "A warm Korean stew built from aged kimchi, pork broth, tofu, and chili heat. It restores energy with deep fermented umami.",
        500,
        27,
        ink,
        False,
        8,
    )

    for i, (label, value) in enumerate([("kcal", "623"), ("price", "9,500 KRW"), ("time", "8 min"), ("balance", "88")]):
        x = 594 + i * 132
        d.rounded_rectangle((x, 448, x + 116, 510), radius=20, fill=(235, 247, 241), outline=(172, 211, 198), width=2)
        text(d, (x + 58, 468), value, 22 if i != 1 else 18, deep, True, anchor="mm")
        text(d, (x + 58, 492), label, 17, (78, 103, 94), False, anchor="mm")

    bot = rounded(fit_crop(source_bot_crop(), (430, 430)), 28)
    im.paste(bot, (72, 570), bot)
    d.rounded_rectangle((72, 570, 502, 1000), radius=28, outline=(70, 153, 128), width=3)

    d.rounded_rectangle((545, 560, 1150, 1015), radius=26, fill=(238, 248, 243), outline=(165, 207, 193), width=3)
    text(d, (580, 596), "KIMCHI JJIGAE FOT", 34, deep, True)
    sections = [
        ("ROLE", "Energy Restorer", "Warms the body and refills daily focus."),
        ("ENERGY", "Warm · Spicy · Focus", "Comforting heat with fermented depth."),
        ("PERSONALITY", "Friendly & hearty", "A reliable companion with bold flavor."),
    ]
    yy = 660
    for title, head, body in sections:
        text(d, (582, yy), title, 23, green, True)
        text(d, (582, yy + 30), head, 23, ink, True)
        yy = multiline(d, (582, yy + 62), body, 500, 21, ink, False, 3) + 18

    d.rounded_rectangle((48, 1048, 548, 1198), radius=26, fill=(238, 248, 243), outline=(165, 207, 193), width=3)
    text(d, (82, 1082), "LUNCH BALANCE", 30, deep, True)
    d.ellipse((92, 1115, 182, 1205), outline=(42, 171, 139), width=14)
    text(d, (137, 1149), "88", 36, deep, True, anchor="mm")
    text(d, (137, 1178), "/100", 20, deep, True, anchor="mm")
    multiline(d, (215, 1125), "Protein 85 · Carb 75 · Fat 55\nFiber 70 · Vitamin 80 · Sodium 40", 295, 20, ink, False, 4)

    d.rounded_rectangle((590, 1048, 1150, 1198), radius=26, fill=(238, 248, 243), outline=(165, 207, 193), width=3)
    text(d, (626, 1082), "SERVICES", 30, deep, True)
    x = 626
    for label in ["Delivery", "Nutrition", "Map", "Save"]:
        x = chip_small(d, (x, 1132), label, green, w=118)

    d.rounded_rectangle((30, 1233, W - 30, 1288), radius=26, fill=green)
    text(d, (W / 2, 1261), "Real Food. Real Energy.", 25, (255, 255, 255), True, anchor="mm")
    return im


def make_recipe():
    orange = (236, 113, 33)
    deep = (144, 61, 18)
    brown = (74, 43, 24)
    im, d = card_base(orange, deep)

    text(d, (58, 51), "MaAM RECIPE", 29, (255, 242, 226), True)
    text(d, (58, 82), "LR TYPE · LINKED RECIPE", 21, (255, 228, 203), False)

    food = rounded(fit_crop(source_food_crop(), (500, 360)), 28)
    im.paste(food, (48, 158), food)
    d.rounded_rectangle((48, 158, 548, 518), radius=28, outline=(228, 132, 64), width=4)

    text(d, (590, 160), "김치찌개", 68, (24, 24, 22), True)
    text(d, (594, 234), "RECIPE CARD", 32, orange, True)
    multiline(
        d,
        (594, 292),
        "숙성 김치의 산미, 돼지고기의 지방감, 두부의 부드러운 질감을 한 냄비에서 균형 있게 끌어내는 제조형 카드입니다.",
        500,
        28,
        brown,
        False,
        10,
    )

    x = 594
    y = 430
    for label, width in [("2인분", 118), ("25분", 118), ("난이도 쉬움", 160)]:
        x = chip_small(d, (x, y), label, orange, w=width)
    chip_small(d, (594, 478), "예상 9,500원", orange, w=180)

    # Ingredients
    d.rounded_rectangle((48, 560, 548, 1015), radius=26, fill=(255, 244, 231), outline=(239, 178, 130), width=3)
    text(d, (80, 592), "재료 체크리스트", 34, deep, True)
    ingredients = [
        ("묵은지", "300g"),
        ("돼지고기 앞다리/목살", "180g"),
        ("두부", "1/2모"),
        ("대파·고추·양파", "적당량"),
        ("멸치육수 또는 물", "600ml"),
        ("고춧가루·다진마늘", "각 1T"),
    ]
    yy = 658
    for name, amount in ingredients:
        d.ellipse((82, yy + 7, 102, yy + 27), fill=orange)
        text(d, (118, yy), name, 27, brown, True)
        text(d, (508, yy), amount, 25, deep, False, anchor="ra")
        yy += 54

    # Process
    d.rounded_rectangle((590, 560, 1150, 885), radius=26, fill=(255, 244, 231), outline=(239, 178, 130), width=3)
    text(d, (626, 592), "조리 공정", 34, deep, True)
    steps = [
        ("01", "김치와 돼지고기를 먼저 볶아 산미와 지방을 결합"),
        ("02", "육수를 붓고 중불에서 15분간 맛을 압축"),
        ("03", "두부와 대파를 넣어 질감과 향을 정리"),
        ("04", "간을 보고 밥과 함께 제공"),
    ]
    yy = 652
    for no, desc in steps:
        d.rounded_rectangle((626, yy, 682, yy + 42), radius=18, fill=orange)
        text(d, (654, yy + 21), no, 21, (255, 255, 255), True, anchor="mm")
        multiline(d, (702, yy + 1), desc, 405, 25, brown, False, 4)
        yy += 58

    # Market links and QR
    d.rounded_rectangle((590, 920, 1150, 1198), radius=26, fill=(255, 244, 231), outline=(239, 178, 130), width=3)
    text(d, (626, 952), "장보기 연결", 34, deep, True)
    x = 626
    y = 1006
    x = chip_small(d, (x, y), "이마트", (199, 80, 24), w=130)
    chip_small(d, (x, y), "온라인 정육점", (199, 80, 24), w=185)
    chip_small(d, (626, y + 52), "가격비교", (199, 80, 24), w=145)
    qr = qr_image("maam://recipe/001-kimchi-jjigae?market=emart&meat=online", 150, deep)
    im.paste(qr, (952, 1026))
    text(d, (1027, 1190), "재료 구매 QR", 22, deep, True, anchor="mm")

    d.rounded_rectangle((48, 1050, 548, 1198), radius=26, fill=(255, 244, 231), outline=(239, 178, 130), width=3)
    text(d, (80, 1082), "제조 포인트", 32, deep, True)
    multiline(d, (80, 1130), "김치를 먼저 볶으면 산미가 둥글어지고, 돼지고기 지방이 국물의 바디감을 만듭니다.", 430, 22, brown, False, 3)

    d.rounded_rectangle((30, 1233, W - 30, 1288), radius=26, fill=orange)
    text(d, (W / 2, 1261), "Cookable Food. Smart Shopping.", 25, (255, 255, 255), True, anchor="mm")
    return im


def make_fine_dining():
    purple = (122, 71, 196)
    deep = (72, 36, 128)
    ink = (35, 28, 45)
    im, d = card_base(purple, deep)

    text(d, (58, 51), "MaAM FINE DINING", 29, (246, 237, 255), True)
    text(d, (58, 82), "LF TYPE · LOCAL FINE DINING", 21, (230, 214, 255), False)

    food = rounded(fit_crop(source_food_crop(), (500, 360)), 28)
    im.paste(food, (48, 158), food)
    d.rounded_rectangle((48, 158, 548, 518), radius=28, outline=(153, 116, 212), width=4)

    text(d, (590, 160), "김치찌개", 68, (24, 24, 22), True)
    text(d, (594, 234), "FINE DINING NOTE", 31, purple, True)
    multiline(
        d,
        (594, 292),
        "숙성 김치의 발효 산미와 돼지고기 육수의 농후함을 조율한 한국식 스튜. 매콤함, 감칠맛, 지방감이 긴 여운으로 이어집니다.",
        505,
        28,
        ink,
        False,
        10,
    )

    x = 594
    y = 440
    for label in ["번역", "맛집검색", "지도앱", "예약"]:
        x = chip(d, (x, y), label, purple, w=120)

    d.rounded_rectangle((48, 560, 548, 1015), radius=26, fill=(248, 242, 255), outline=(178, 151, 221), width=3)
    text(d, (80, 592), "테이스팅 구조", 34, deep, True)
    bars = [
        ("Fermentation", "발효 산미", 88, (130, 77, 202)),
        ("Umami", "감칠맛", 92, (106, 87, 196)),
        ("Spice", "매콤함", 74, (170, 80, 162)),
        ("Body", "국물 농도", 82, (112, 71, 150)),
        ("Finish", "여운", 80, (99, 76, 166)),
    ]
    yy = 662
    for en, ko, val, c in bars:
        text(d, (82, yy), ko, 25, ink, True)
        text(d, (215, yy + 2), en, 18, (99, 87, 116), False)
        d.rounded_rectangle((82, yy + 34, 460, yy + 52), radius=9, fill=(229, 222, 241))
        d.rounded_rectangle((82, yy + 34, 82 + int(378 * val / 100), yy + 52), radius=9, fill=c)
        text(d, (500, yy + 44), str(val), 21, deep, True, anchor="mm")
        yy += 70

    d.rounded_rectangle((590, 560, 1150, 885), radius=26, fill=(248, 242, 255), outline=(178, 151, 221), width=3)
    text(d, (626, 592), "파인다이닝 해석", 34, deep, True)
    bullets = [
        "육수: 지방과 김치 국물의 균형",
        "질감: 두부와 김치 섬유감",
        "향: 파, 고추, 발효향의 레이어",
        "페어링: 쌀밥, 막걸리, 라거",
    ]
    yy = 652
    for b in bullets:
        d.ellipse((626, yy + 9, 642, yy + 25), fill=purple)
        yy = multiline(d, (658, yy), b, 430, 23, ink, False, 3) + 10

    d.rounded_rectangle((48, 1050, 548, 1198), radius=26, fill=(248, 242, 255), outline=(178, 151, 221), width=3)
    text(d, (80, 1082), "영문 설명", 32, deep, True)
    multiline(d, (80, 1130), "A fermented kimchi stew with layered acidity, pork broth depth, tofu softness, and spicy umami.", 430, 19, ink, False, 2)

    d.rounded_rectangle((590, 920, 1150, 1198), radius=26, fill=(248, 242, 255), outline=(178, 151, 221), width=3)
    text(d, (626, 952), "QR 서비스 허브", 34, deep, True)
    qr_url = "https://www.google.com/maps/search/" + quote("김치찌개 맛집")
    qr = qr_image(qr_url, 168, deep)
    im.paste(qr, (942, 998))
    x = 626
    y = 1008
    x = chip_small(d, (x, y), "지도 검색", purple, w=126)
    chip_small(d, (x, y), "메뉴 번역", purple, w=126)
    chip_small(d, (626, y + 50), "리뷰 보기", purple, w=126)
    multiline(d, (626, 1142), "QR을 스캔하면 주변 김치찌개 맛집 검색으로 연결됩니다.", 270, 19, ink, False, 2)

    d.rounded_rectangle((30, 1233, W - 30, 1288), radius=26, fill=purple)
    text(d, (W / 2, 1261), "Taste Beyond Menu. Search Beyond Card.", 25, (255, 255, 255), True, anchor="mm")
    return im


def make_compare(recipe, fine):
    lm = Image.open(SOURCE).convert("RGB")
    thumbs = []
    for im in [lm, recipe, fine]:
        t = im.copy()
        t.thumbnail((420, 460), Image.Resampling.LANCZOS)
        thumbs.append(t)
    labels = [
        ("GREEN LM CARD", "음식 + 캐릭터 식별"),
        ("ORANGE LR CARD", "제조 + 장보기 연결"),
        ("PURPLE LF CARD", "해석 + 번역 + 지도 QR"),
    ]
    sheet = Image.new("RGB", (1380, 575), (246, 244, 238))
    d = ImageDraw.Draw(sheet)
    for i, (thumb, (title, desc)) in enumerate(zip(thumbs, labels)):
        x = 30 + i * 450
        d.rounded_rectangle((x, 24, x + 420, 548), radius=24, fill=(255, 255, 255), outline=(210, 205, 195), width=2)
        text(d, (x + 24, 46), title, 25, (22, 74, 62), True)
        text(d, (x + 24, 78), desc, 22, (83, 77, 68), False)
        sheet.paste(thumb, (x + (420 - thumb.width) // 2, 112))
    return sheet


def make_recipe_en():
    orange = (236, 113, 33)
    deep = (144, 61, 18)
    brown = (74, 43, 24)
    im, d = card_base(orange, deep)

    text(d, (58, 51), "MaAM RECIPE", 29, (255, 242, 226), True)
    text(d, (58, 82), "LR TYPE · LINKED RECIPE", 21, (255, 228, 203), False)

    food = rounded(fit_crop(source_food_crop(), (500, 360)), 28)
    im.paste(food, (48, 158), food)
    d.rounded_rectangle((48, 158, 548, 518), radius=28, outline=(228, 132, 64), width=4)

    text(d, (590, 160), "KIMCHI JJIGAE", 58, (24, 24, 22), True)
    text(d, (594, 224), "김치찌개", 34, orange, True)
    text(d, (594, 266), "RECIPE CARD", 30, orange, True)
    multiline(
        d,
        (594, 318),
        "A cookable card for balancing aged kimchi acidity, pork richness, tofu softness, and chili heat in one pot.",
        500,
        27,
        brown,
        False,
        8,
    )

    x = 594
    y = 442
    for label, width in [("2 servings", 142), ("25 min", 120), ("Easy", 104)]:
        x = chip_small(d, (x, y), label, orange, w=width)
    chip_small(d, (594, 490), "Est. 9,500 KRW", orange, w=190)

    d.rounded_rectangle((48, 560, 548, 1015), radius=26, fill=(255, 244, 231), outline=(239, 178, 130), width=3)
    text(d, (80, 592), "Ingredient Checklist", 32, deep, True)
    ingredients = [
        ("Aged kimchi", "300g"),
        ("Pork shoulder or neck", "180g"),
        ("Tofu", "1/2 block"),
        ("Scallion · chili · onion", "to taste"),
        ("Anchovy stock or water", "600ml"),
        ("Chili flakes · garlic", "1 tbsp each"),
    ]
    yy = 658
    for name, amount in ingredients:
        d.ellipse((82, yy + 7, 102, yy + 27), fill=orange)
        text(d, (118, yy), name, 24, brown, True)
        text(d, (508, yy), amount, 22, deep, False, anchor="ra")
        yy += 54

    d.rounded_rectangle((590, 560, 1150, 885), radius=26, fill=(255, 244, 231), outline=(239, 178, 130), width=3)
    text(d, (626, 592), "Cooking Flow", 34, deep, True)
    steps = [
        ("01", "Stir-fry kimchi and pork to bind acidity and fat"),
        ("02", "Add stock and simmer 15 minutes over medium heat"),
        ("03", "Add tofu and scallion to finish texture and aroma"),
        ("04", "Adjust seasoning and serve with rice"),
    ]
    yy = 652
    for no, desc in steps:
        d.rounded_rectangle((626, yy, 682, yy + 42), radius=18, fill=orange)
        text(d, (654, yy + 21), no, 21, (255, 255, 255), True, anchor="mm")
        multiline(d, (702, yy + 1), desc, 405, 22, brown, False, 3)
        yy += 58

    d.rounded_rectangle((590, 920, 1150, 1198), radius=26, fill=(255, 244, 231), outline=(239, 178, 130), width=3)
    text(d, (626, 952), "Shopping Links", 34, deep, True)
    x = chip_small(d, (626, 1008), "E-Mart", (199, 80, 24), w=120)
    chip_small(d, (x, 1008), "Online butcher", (199, 80, 24), w=185)
    chip_small(d, (626, 1060), "Price compare", (199, 80, 24), w=170)
    qr = qr_image("maam://recipe/001-kimchi-jjigae?lang=en&market=emart&meat=online", 150, deep)
    im.paste(qr, (952, 1026))
    text(d, (1027, 1182), "SHOP QR", 20, deep, True, anchor="mm")

    d.rounded_rectangle((48, 1050, 548, 1198), radius=26, fill=(255, 244, 231), outline=(239, 178, 130), width=3)
    text(d, (80, 1082), "Production Point", 31, deep, True)
    multiline(d, (80, 1130), "Frying kimchi first rounds the acidity and lets pork fat build the broth body.", 430, 23, brown, False, 3)

    d.rounded_rectangle((30, 1233, W - 30, 1288), radius=26, fill=orange)
    text(d, (W / 2, 1261), "Cookable Food. Smart Shopping.", 25, (255, 255, 255), True, anchor="mm")
    return im


def make_fine_dining_en():
    purple = (122, 71, 196)
    deep = (72, 36, 128)
    ink = (35, 28, 45)
    im, d = card_base(purple, deep)

    text(d, (58, 51), "MaAM FINE DINING", 29, (246, 237, 255), True)
    text(d, (58, 82), "LF TYPE · LOCAL FINE DINING", 21, (230, 214, 255), False)

    food = rounded(fit_crop(source_food_crop(), (500, 360)), 28)
    im.paste(food, (48, 158), food)
    d.rounded_rectangle((48, 158, 548, 518), radius=28, outline=(153, 116, 212), width=4)

    text(d, (590, 160), "KIMCHI JJIGAE", 58, (24, 24, 22), True)
    text(d, (594, 224), "김치찌개", 34, purple, True)
    text(d, (594, 266), "FINE DINING NOTE", 30, purple, True)
    multiline(
        d,
        (594, 318),
        "A Korean fermented stew tuned around aged kimchi acidity, pork broth depth, tofu softness, and a long spicy umami finish.",
        505,
        27,
        ink,
        False,
        8,
    )

    x = 594
    y = 456
    for label in ["Translate", "Restaurant", "Map", "Reserve"]:
        x = chip_small(d, (x, y), label, purple, w=126)

    d.rounded_rectangle((48, 560, 548, 1015), radius=26, fill=(248, 242, 255), outline=(178, 151, 221), width=3)
    text(d, (80, 592), "Tasting Structure", 32, deep, True)
    bars = [
        ("Fermentation", "Fermented acidity", 88, (130, 77, 202)),
        ("Umami", "Savory depth", 92, (106, 87, 196)),
        ("Spice", "Chili heat", 74, (170, 80, 162)),
        ("Body", "Broth weight", 82, (112, 71, 150)),
        ("Finish", "Aftertaste", 80, (99, 76, 166)),
    ]
    yy = 662
    for en, label, val, c in bars:
        text(d, (82, yy), label, 23, ink, True)
        text(d, (330, yy + 2), en, 16, (99, 87, 116), False)
        d.rounded_rectangle((82, yy + 34, 460, yy + 52), radius=9, fill=(229, 222, 241))
        d.rounded_rectangle((82, yy + 34, 82 + int(378 * val / 100), yy + 52), radius=9, fill=c)
        text(d, (500, yy + 44), str(val), 21, deep, True, anchor="mm")
        yy += 70

    d.rounded_rectangle((590, 560, 1150, 885), radius=26, fill=(248, 242, 255), outline=(178, 151, 221), width=3)
    text(d, (626, 592), "Dining Interpretation", 31, deep, True)
    bullets = [
        "Broth: balance of pork fat and kimchi liquor",
        "Texture: soft tofu and fibrous kimchi",
        "Aroma: scallion, chili, fermented layers",
        "Pairing: steamed rice, makgeolli, light lager",
    ]
    yy = 652
    for b in bullets:
        d.ellipse((626, yy + 9, 642, yy + 25), fill=purple)
        yy = multiline(d, (658, yy), b, 430, 21, ink, False, 3) + 10

    d.rounded_rectangle((48, 1050, 548, 1198), radius=26, fill=(248, 242, 255), outline=(178, 151, 221), width=3)
    text(d, (80, 1082), "Korean Name", 31, deep, True)
    text(d, (80, 1136), "김치찌개", 45, ink, True)

    d.rounded_rectangle((590, 920, 1150, 1198), radius=26, fill=(248, 242, 255), outline=(178, 151, 221), width=3)
    text(d, (626, 952), "QR Service Hub", 32, deep, True)
    qr_url = "https://www.google.com/maps/search/" + quote("kimchi jjigae restaurant near me")
    qr = qr_image(qr_url, 168, deep)
    im.paste(qr, (942, 998))
    x = chip_small(d, (626, 1008), "Map Search", purple, w=130)
    chip_small(d, (x, 1008), "Translate", purple, w=130)
    chip_small(d, (626, 1058), "Reviews", purple, w=126)
    multiline(d, (626, 1142), "Scan to search nearby restaurants serving kimchi jjigae.", 270, 19, ink, False, 2)

    d.rounded_rectangle((30, 1233, W - 30, 1288), radius=26, fill=purple)
    text(d, (W / 2, 1261), "Taste Beyond Menu. Search Beyond Card.", 25, (255, 255, 255), True, anchor="mm")
    return im


def make_compare_en(lm, recipe, fine):
    thumbs = []
    for im in [lm, recipe, fine]:
        t = im.copy()
        t.thumbnail((420, 460), Image.Resampling.LANCZOS)
        thumbs.append(t)
    labels = [
        ("GREEN LM CARD", "food + character result"),
        ("ORANGE LR CARD", "recipe + shopping links"),
        ("PURPLE LF CARD", "dining note + map QR"),
    ]
    sheet = Image.new("RGB", (1380, 575), (246, 244, 238))
    d = ImageDraw.Draw(sheet)
    for i, (thumb, (title, desc)) in enumerate(zip(thumbs, labels)):
        x = 30 + i * 450
        d.rounded_rectangle((x, 24, x + 420, 548), radius=24, fill=(255, 255, 255), outline=(210, 205, 195), width=2)
        text(d, (x + 24, 46), title, 25, (22, 74, 62), True)
        text(d, (x + 24, 78), desc, 22, (83, 77, 68), False)
        sheet.paste(thumb, (x + (420 - thumb.width) // 2, 112))
    return sheet


def main():
    (OUT / "lm").mkdir(parents=True, exist_ok=True)
    (OUT / "recipe").mkdir(parents=True, exist_ok=True)
    (OUT / "fine_dining").mkdir(parents=True, exist_ok=True)
    (OUT / "compare").mkdir(parents=True, exist_ok=True)

    lm_dest = OUT / "lm" / "001_kmj_lm.png"
    Image.open(SOURCE).save(lm_dest)

    recipe = make_recipe()
    fine = make_fine_dining()
    recipe_path = OUT / "recipe" / "001_kmj_lr_recipe.png"
    fine_path = OUT / "fine_dining" / "001_kmj_lf_fine_dining.png"
    compare_path = OUT / "compare" / "001_kmj_three_card_compare.png"
    recipe.save(recipe_path, quality=95)
    fine.save(fine_path, quality=95)
    make_compare(recipe, fine).save(compare_path, quality=92)

    lm_en = make_lm_en()
    recipe_en = make_recipe_en()
    fine_en = make_fine_dining_en()
    lm_en_path = OUT / "lm" / "001_kmj_lm_en.png"
    recipe_en_path = OUT / "recipe" / "001_kmj_lr_recipe_en.png"
    fine_en_path = OUT / "fine_dining" / "001_kmj_lf_fine_dining_en.png"
    compare_en_path = OUT / "compare" / "001_kmj_three_card_compare_en.png"
    lm_en.save(lm_en_path, quality=95)
    recipe_en.save(recipe_en_path, quality=95)
    fine_en.save(fine_en_path, quality=95)
    make_compare_en(lm_en, recipe_en, fine_en).save(compare_en_path, quality=92)

    print(lm_dest)
    print(recipe_path)
    print(fine_path)
    print(compare_path)
    print(lm_en_path)
    print(recipe_en_path)
    print(fine_en_path)
    print(compare_en_path)


if __name__ == "__main__":
    main()
