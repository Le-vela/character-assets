from pathlib import Path
from urllib.parse import quote

import qrcode
from PIL import Image, ImageDraw, ImageFont, ImageOps


ROOT = Path(r"C:\Discovery\Cosmo\dev\lab\utility\card")
LM_SRC = Path(r"C:\Discovery\Cosmo\dev\maker-and-made\data\images\lm")
OUT = ROOT / "output"
ASSET_CARD = Path(r"C:\Discovery\Ocean\dev\character-assets\card")

W, H = 1198, 1313
FONT_REG = r"C:\Windows\Fonts\malgun.ttf"
FONT_BOLD = r"C:\Windows\Fonts\malgunbd.ttf"


MENU = [
    {
        "id": "001",
        "code": "kmj",
        "ko": "김치찌개",
        "en": "KIMCHI STEW",
        "desc": "A cookable card for balancing aged kimchi acidity, pork richness, tofu softness, and chili heat in one pot.",
        "servings": "2 servings",
        "time": "25 min",
        "level": "Easy",
        "cost": "Est. 9,500 KRW",
        "ingredients": [("Aged kimchi", "300g"), ("Pork shoulder or neck", "180g"), ("Tofu", "1/2 block"), ("Scallion, chili, onion", "to taste"), ("Anchovy stock or water", "600ml"), ("Chili flakes, garlic", "1 tbsp each")],
        "steps": ["Stir-fry kimchi and pork to bind acidity and fat", "Add stock and simmer 15 minutes over medium heat", "Add tofu and scallion to finish texture and aroma", "Adjust seasoning and serve with rice"],
        "point": "Frying kimchi first rounds the acidity and lets pork fat build the broth body.",
        "dining": "A Korean fermented stew tuned around aged kimchi acidity, pork broth depth, tofu softness, and a long spicy umami finish.",
        "taste": [("Fermented acidity", "Fermentation", 88), ("Savory depth", "Umami", 92), ("Chili heat", "Spice", 74), ("Broth weight", "Body", 82), ("Aftertaste", "Finish", 80)],
        "notes": ["Broth: balance of pork fat and kimchi liquor", "Texture: soft tofu and fibrous kimchi", "Banchan: free side dishes, often refillable", "Pairing: steamed rice, makgeolli, light lager"],
    },
    {
        "id": "002",
        "code": "dnj",
        "ko": "된장찌개",
        "en": "DOENJANG STEW",
        "desc": "A soybean paste stew card built around earthy jang, tofu, squash, mushrooms, and clean vegetable sweetness.",
        "servings": "2 servings",
        "time": "22 min",
        "level": "Easy",
        "cost": "Est. 8,000 KRW",
        "ingredients": [("Doenjang paste", "2 tbsp"), ("Tofu", "1/2 block"), ("Zucchini and onion", "160g"), ("Mushrooms", "80g"), ("Anchovy kelp stock", "650ml"), ("Chili and scallion", "to taste")],
        "steps": ["Dissolve doenjang into hot stock", "Add firm vegetables and simmer until sweet", "Add tofu and mushrooms near the end", "Finish with scallion and chili"],
        "point": "Do not boil the paste too aggressively; a steady simmer keeps the soybean aroma clean.",
        "dining": "A rustic fermented soybean stew with mineral depth, nutty aroma, and a calm savory finish.",
        "taste": [("Soybean aroma", "Fermentation", 86), ("Savory broth", "Umami", 84), ("Gentle heat", "Spice", 45), ("Comforting body", "Body", 76), ("Nutty finish", "Finish", 82)],
        "notes": ["Broth: doenjang dissolved in anchovy kelp stock", "Texture: tofu, zucchini, mushroom", "Aroma: soybean paste, scallion, chili", "Pairing: barley rice, grilled fish, banchan"],
    },
    {
        "id": "003",
        "code": "bbp",
        "ko": "비빔밥",
        "en": "BIBIMBAP",
        "desc": "A bowl assembly card for rice, seasoned vegetables, protein, gochujang, sesame oil, and a glossy egg finish.",
        "servings": "1 serving",
        "time": "18 min",
        "level": "Easy",
        "cost": "Est. 8,200 KRW",
        "ingredients": [("Cooked rice", "210g"), ("Assorted namul", "220g"), ("Ground beef or tofu", "80g"), ("Egg yolk or fried egg", "1"), ("Gochujang sauce", "1.5 tbsp"), ("Sesame oil", "1 tsp")],
        "steps": ["Warm rice and arrange vegetables by color", "Cook protein with light seasoning", "Place egg and gochujang in the center", "Mix with sesame oil just before eating"],
        "point": "Keep each topping distinct before mixing so color, texture, and seasoning stay balanced.",
        "dining": "A composed rice bowl where color, crunch, sauce, and sesame aroma become one tableside.",
        "taste": [("Vegetable freshness", "Freshness", 90), ("Gochujang depth", "Umami", 78), ("Sauce heat", "Spice", 62), ("Rice body", "Body", 74), ("Sesame aroma", "Finish", 88)],
        "notes": ["Base: warm rice with seasonal vegetables", "Texture: crisp, soft, chewy layers", "Aroma: sesame oil, gochujang, namul", "Pairing: clear soup, barley tea, light lager"],
    },
    {
        "id": "004",
        "code": "sdf",
        "ko": "순두부찌개",
        "en": "SOFT TOFU STEW",
        "desc": "A soft tofu stew card focused on silky curds, spicy broth, egg richness, and quick simmered seafood or pork.",
        "servings": "2 servings",
        "time": "18 min",
        "level": "Easy",
        "cost": "Est. 7,800 KRW",
        "ingredients": [("Soft tofu", "1 tube"), ("Pork or seafood", "120g"), ("Chili oil base", "1 tbsp"), ("Egg", "1"), ("Stock", "500ml"), ("Scallion and chili", "to taste")],
        "steps": ["Bloom chili oil with aromatics", "Add protein and stock, then simmer", "Slide in soft tofu without breaking it too much", "Crack egg on top and serve bubbling"],
        "point": "Add tofu late and keep the curds large for a soft, custard-like spoonful.",
        "dining": "A bubbling stew with delicate tofu texture, bright chili oil, and a rounded egg finish.",
        "taste": [("Soft tofu", "Texture", 92), ("Broth savor", "Umami", 80), ("Chili oil", "Spice", 76), ("Light body", "Body", 68), ("Clean finish", "Finish", 72)],
        "notes": ["Broth: chili oil and seafood or pork stock", "Texture: silky tofu and soft egg", "Aroma: chili, scallion, sesame", "Pairing: steamed rice, pickles, cold barley tea"],
    },
    {
        "id": "005",
        "code": "jyk",
        "ko": "제육볶음",
        "en": "JEYUK BOKKEUM",
        "desc": "A stir-fry card for pork slices coated in sweet spicy gochujang sauce with onion, scallion, and sesame.",
        "servings": "2 servings",
        "time": "20 min",
        "level": "Medium",
        "cost": "Est. 8,500 KRW",
        "ingredients": [("Pork shoulder slices", "250g"), ("Onion and scallion", "180g"), ("Gochujang", "1.5 tbsp"), ("Soy sauce", "1 tbsp"), ("Sugar or syrup", "1 tbsp"), ("Garlic and sesame", "to taste")],
        "steps": ["Mix pork with sauce and rest briefly", "Sear over high heat to brown edges", "Add vegetables and toss until glossy", "Finish with sesame and serve with rice"],
        "point": "High heat creates charred edges while keeping the sauce sticky, not watery.",
        "dining": "A fiery pork plate with caramelized sauce, grilled edges, and a punchy rice-friendly finish.",
        "taste": [("Charred pork", "Maillard", 86), ("Sauce savor", "Umami", 78), ("Sweet heat", "Spice", 84), ("Meaty body", "Body", 88), ("Sesame finish", "Finish", 70)],
        "notes": ["Sauce: gochujang, soy, garlic, sweetness", "Texture: chewy pork and soft onion", "Aroma: grill char, chili, sesame", "Pairing: lettuce wraps, rice, cold beer"],
    },
    {
        "id": "006",
        "code": "dks",
        "ko": "돈까스",
        "en": "DONKATSU",
        "desc": "A cutlet card for juicy pork, crisp panko crust, cabbage salad, rice, and sweet savory sauce.",
        "servings": "1 serving",
        "time": "25 min",
        "level": "Medium",
        "cost": "Est. 9,500 KRW",
        "ingredients": [("Pork loin cutlet", "180g"), ("Flour, egg, panko", "1 set"), ("Cabbage", "80g"), ("Rice", "1 bowl"), ("Tonkatsu sauce", "3 tbsp"), ("Oil", "for frying")],
        "steps": ["Pound and season the pork evenly", "Coat with flour, egg, and panko", "Fry until golden and rest briefly", "Slice and serve with sauce and cabbage"],
        "point": "Resting after frying keeps juices inside and helps the crust stay crisp.",
        "dining": "A comfort cutlet where crisp panko, tender pork, and tangy sauce create a clean contrast.",
        "taste": [("Crisp crust", "Texture", 90), ("Pork savor", "Umami", 72), ("Sauce tang", "Acidity", 65), ("Fried body", "Body", 86), ("Clean finish", "Finish", 62)],
        "notes": ["Crust: panko fried to a dry crisp", "Texture: juicy pork and shredded cabbage", "Aroma: toasted crumb, sauce, mustard", "Pairing: rice, miso soup, pickles"],
    },
    {
        "id": "007",
        "code": "gks",
        "ko": "국수",
        "en": "KOREAN NOODLES",
        "desc": "A flexible noodle card for light anchovy broth or spicy mixed sauce, thin noodles, vegetables, and egg.",
        "servings": "1 serving",
        "time": "12 min",
        "level": "Easy",
        "cost": "Est. 6,500 KRW",
        "ingredients": [("Somyeon noodles", "100g"), ("Anchovy broth or sauce", "1 portion"), ("Cucumber or zucchini", "60g"), ("Egg garnish", "1/2"), ("Kimchi", "optional"), ("Sesame and scallion", "to taste")],
        "steps": ["Boil noodles and rinse for springy texture", "Warm broth or mix spicy sauce", "Add garnish and seasoning", "Serve immediately before noodles soften"],
        "point": "Rinsing cooked noodles quickly removes starch and keeps the bite clean.",
        "dining": "A quick noodle bowl with a clean slurp, simple garnish, and either gentle broth or bright spice.",
        "taste": [("Noodle spring", "Texture", 82), ("Broth clarity", "Umami", 70), ("Sauce heat", "Spice", 58), ("Light body", "Body", 56), ("Refreshing finish", "Finish", 78)],
        "notes": ["Base: somyeon with broth or bibim sauce", "Texture: thin, springy noodles", "Aroma: sesame, scallion, anchovy", "Pairing: kimchi, dumplings, iced tea"],
    },
    {
        "id": "008",
        "code": "nmy",
        "ko": "냉면",
        "en": "NAENGMYEON",
        "desc": "A chilled noodle card for icy broth, chewy buckwheat noodles, cucumber, pear, egg, and mustard vinegar lift.",
        "servings": "1 serving",
        "time": "15 min",
        "level": "Easy",
        "cost": "Est. 9,000 KRW",
        "ingredients": [("Naengmyeon noodles", "1 bundle"), ("Cold beef broth", "350ml"), ("Cucumber and pear", "80g"), ("Boiled egg", "1/2"), ("Mustard and vinegar", "to taste"), ("Ice", "as needed")],
        "steps": ["Boil noodles briefly and rinse until cold", "Chill broth with ice", "Arrange garnish neatly", "Season tableside with mustard and vinegar"],
        "point": "Extreme rinsing gives naengmyeon its cold, elastic bite.",
        "dining": "A cold noodle dish defined by icy clarity, chewy strands, pear sweetness, and sharp mustard vinegar.",
        "taste": [("Cold clarity", "Freshness", 92), ("Broth savor", "Umami", 70), ("Mustard lift", "Spice", 50), ("Chewy body", "Body", 66), ("Clean finish", "Finish", 90)],
        "notes": ["Broth: chilled beef or dongchimi style", "Texture: elastic buckwheat noodles", "Aroma: pear, mustard, vinegar", "Pairing: grilled meat, dumplings, cold water"],
    },
    {
        "id": "009",
        "code": "sgs",
        "ko": "삼겹살 구이",
        "en": "GRILLED SAMGYEOPSAL",
        "desc": "A grill card for pork belly, lettuce wraps, garlic, ssamjang, kimchi, and shared table energy.",
        "servings": "2 servings",
        "time": "30 min",
        "level": "Medium",
        "cost": "Est. 18,000 KRW",
        "ingredients": [("Pork belly", "400g"), ("Lettuce and perilla", "1 set"), ("Garlic and chili", "to taste"), ("Ssamjang", "3 tbsp"), ("Kimchi", "150g"), ("Rice or fried rice", "optional")],
        "steps": ["Heat grill and lay pork belly flat", "Render fat until edges crisp", "Grill garlic and kimchi beside pork", "Wrap with greens and sauce"],
        "point": "Let the fat render slowly before crisping; that gives the best grilled aroma.",
        "dining": "A social grill plate driven by rendered pork fat, crisp edges, fresh wraps, and fermented accents.",
        "taste": [("Grill aroma", "Maillard", 92), ("Pork richness", "Umami", 86), ("Garlic bite", "Spice", 55), ("Fatty body", "Body", 94), ("Fresh finish", "Finish", 65)],
        "notes": ["Grill: rendered belly with crisp edges", "Texture: fatty pork and fresh leaves", "Aroma: smoke, garlic, grilled kimchi", "Pairing: ssam, soju, cold noodles"],
    },
    {
        "id": "010",
        "code": "dgb",
        "ko": "닭갈비",
        "en": "DAKGALBI",
        "desc": "A spicy chicken griddle card with cabbage, sweet potato, rice cakes, perilla leaves, and a bold red sauce.",
        "servings": "2 servings",
        "time": "28 min",
        "level": "Medium",
        "cost": "Est. 11,000 KRW",
        "ingredients": [("Chicken thigh", "300g"), ("Cabbage and onion", "220g"), ("Sweet potato", "100g"), ("Rice cakes", "100g"), ("Gochujang sauce", "3 tbsp"), ("Perilla leaves", "to taste")],
        "steps": ["Marinate chicken in spicy sauce", "Cook vegetables and chicken on a griddle", "Add rice cakes and sweet potato until tender", "Finish with perilla or fried rice"],
        "point": "Stir often so the sauce caramelizes without burning on the pan.",
        "dining": "A spicy griddle dish with sweet vegetables, chewy rice cakes, and smoky chili chicken.",
        "taste": [("Caramelized sauce", "Maillard", 82), ("Chicken savor", "Umami", 78), ("Chili heat", "Spice", 86), ("Hearty body", "Body", 84), ("Herbal finish", "Finish", 70)],
        "notes": ["Sauce: gochujang, garlic, soy, sweetness", "Texture: tender chicken and chewy tteok", "Aroma: perilla, chili, pan char", "Pairing: fried rice, cheese, cold beer"],
    },
    {
        "id": "011",
        "code": "pho",
        "ko": "쌀국수",
        "en": "PHO",
        "desc": "A Vietnamese noodle card for aromatic broth, rice noodles, herbs, lime, onion, and tender beef or chicken.",
        "servings": "1 serving",
        "time": "20 min",
        "level": "Easy",
        "cost": "Est. 9,500 KRW",
        "ingredients": [("Rice noodles", "100g"), ("Beef or chicken", "100g"), ("Pho broth", "450ml"), ("Onion and sprouts", "100g"), ("Thai basil and cilantro", "to taste"), ("Lime and chili", "to taste")],
        "steps": ["Soak and blanch rice noodles", "Heat broth with aromatic spices", "Add meat, onion, and sprouts", "Finish with herbs, lime, and chili"],
        "point": "Fresh herbs and lime should go in last to keep the broth bright and Vietnamese in character.",
        "dining": "A fragrant Vietnamese bowl balancing star anise broth, soft rice noodles, herbs, lime, and tender meat.",
        "taste": [("Herbal lift", "Freshness", 88), ("Spiced broth", "Aroma", 86), ("Chili option", "Spice", 45), ("Light body", "Body", 64), ("Lime finish", "Finish", 84)],
        "notes": ["Broth: star anise, cinnamon, onion, ginger", "Texture: slippery rice noodles and tender meat", "Aroma: basil, cilantro, lime", "Pairing: spring rolls, iced coffee, chili sauce"],
    },
    {
        "id": "012",
        "code": "mlt",
        "ko": "마라탕",
        "en": "MALATANG",
        "desc": "A custom hot pot card for mala broth, chosen vegetables, tofu, meat, noodles, and numbing spice control.",
        "servings": "1 bowl",
        "time": "18 min",
        "level": "Medium",
        "cost": "Est. 12,000 KRW",
        "ingredients": [("Mala soup base", "1 portion"), ("Assorted vegetables", "250g"), ("Tofu or fish cake", "120g"), ("Meat slices", "100g"), ("Noodles", "optional"), ("Garlic sauce", "to taste")],
        "steps": ["Choose ingredients by texture and weight", "Simmer firm items first in mala broth", "Add delicate greens and noodles last", "Adjust spice, numbness, and sauce"],
        "point": "Balance heavy items with greens so the bowl stays flavorful without becoming greasy.",
        "dining": "A customizable Sichuan-style bowl with numbing pepper, chili oil, layered textures, and personal heat.",
        "taste": [("Mala numbness", "Sensation", 92), ("Chili oil", "Spice", 90), ("Broth savor", "Umami", 72), ("Custom body", "Body", 78), ("Pepper finish", "Finish", 88)],
        "notes": ["Broth: chili oil and Sichuan pepper", "Texture: vegetables, tofu, meat, noodles", "Aroma: garlic, sesame, spices", "Pairing: rice, yogurt drink, iced tea"],
    },
    {
        "id": "013",
        "code": "sdb",
        "ko": "샐러드 보울",
        "en": "SALAD BOWL",
        "desc": "A health bowl card for greens, grains, lean protein, vegetables, nuts, and a bright dressing.",
        "servings": "1 bowl",
        "time": "12 min",
        "level": "Easy",
        "cost": "Est. 10,500 KRW",
        "ingredients": [("Mixed greens", "120g"), ("Grain base", "100g"), ("Chicken, egg, or tofu", "120g"), ("Seasonal vegetables", "180g"), ("Nuts or seeds", "15g"), ("Dressing", "2 tbsp")],
        "steps": ["Dry greens well for crisp volume", "Layer grains and protein for fullness", "Add colorful vegetables and crunch", "Dress lightly just before eating"],
        "point": "Keep dressing separate until the end so greens stay crisp and fresh.",
        "dining": "A clean bowl built around freshness, color, lean protein, grain structure, and controlled dressing.",
        "taste": [("Fresh greens", "Freshness", 94), ("Protein balance", "Umami", 62), ("Dressing lift", "Acidity", 76), ("Light body", "Body", 58), ("Clean finish", "Finish", 90)],
        "notes": ["Base: greens plus grain or beans", "Texture: crisp, creamy, crunchy contrast", "Aroma: herbs, citrus, olive oil", "Pairing: soup, sparkling water, sourdough"],
    },
    {
        "id": "014",
        "code": "sns",
        "ko": "샌드위치 & 수프",
        "en": "SANDWICH & SOUP",
        "desc": "A desk lunch card for layered bread, protein, vegetables, spread, and a warm soup side.",
        "servings": "1 set",
        "time": "10 min",
        "level": "Easy",
        "cost": "Est. 9,000 KRW",
        "ingredients": [("Bread", "2 slices"), ("Turkey, ham, or egg", "100g"), ("Cheese", "1 slice"), ("Lettuce and tomato", "80g"), ("Spread", "1 tbsp"), ("Soup", "1 cup")],
        "steps": ["Toast bread lightly if needed", "Layer spread, protein, cheese, and vegetables", "Press and slice for clean handling", "Serve with warm soup"],
        "point": "Put wetter vegetables away from bread or use a thin spread barrier.",
        "dining": "A compact lunch set where crisp bread, layered filling, and warm soup create practical comfort.",
        "taste": [("Bread texture", "Texture", 78), ("Filling savor", "Umami", 70), ("Soup warmth", "Comfort", 82), ("Medium body", "Body", 68), ("Clean finish", "Finish", 66)],
        "notes": ["Base: bread, protein, vegetables, spread", "Texture: crisp crust and soft filling", "Aroma: toasted bread, soup, herbs", "Pairing: coffee, sparkling water, fruit"],
    },
    {
        "id": "015",
        "code": "sro",
        "ko": "초밥·롤",
        "en": "SUSHI & ROLLS",
        "desc": "A Japanese lunch card for seasoned rice, fish or fillings, seaweed, wasabi, soy sauce, and clean portions.",
        "servings": "1 set",
        "time": "15 min",
        "level": "Medium",
        "cost": "Est. 12,000 KRW",
        "ingredients": [("Sushi rice", "220g"), ("Fish or roll fillings", "160g"), ("Nori", "2 sheets"), ("Cucumber or avocado", "80g"), ("Wasabi", "to taste"), ("Soy sauce and ginger", "1 set")],
        "steps": ["Season rice with vinegar and cool it", "Prepare fillings into even strips", "Roll or shape with gentle pressure", "Serve with soy, wasabi, and ginger"],
        "point": "Rice should be seasoned and warm-room temperature, not cold and hard.",
        "dining": "A precise rice-based set highlighting clean fish, vinegar balance, seaweed aroma, and controlled bites.",
        "taste": [("Rice balance", "Acidity", 82), ("Seafood savor", "Umami", 84), ("Wasabi lift", "Spice", 48), ("Light body", "Body", 60), ("Clean finish", "Finish", 88)],
        "notes": ["Base: vinegared rice and fish or fillings", "Texture: soft rice, clean bite, crisp nori", "Aroma: seaweed, wasabi, ginger", "Pairing: miso soup, green tea, sake"],
    },
    {
        "id": "016",
        "code": "udn",
        "ko": "우동",
        "en": "UDON",
        "desc": "A warm noodle card for thick udon, clear dashi broth, scallion, tempura flakes, fish cake, and seasonal toppings.",
        "servings": "1 bowl",
        "time": "8 min",
        "level": "Easy",
        "cost": "Est. 8,500 KRW",
        "ingredients": [("Udon noodles", "1 pack"), ("Dashi broth", "450ml"), ("Fish cake", "2 slices"), ("Scallion", "to taste"), ("Tempura flakes", "2 tbsp"), ("Soy or tsuyu", "1 tbsp")],
        "steps": ["Heat dashi broth and season lightly", "Warm udon noodles until bouncy", "Add fish cake and scallion", "Finish with tempura flakes just before serving"],
        "point": "Avoid overboiling udon; thick noodles should stay springy and smooth.",
        "dining": "A simple Japanese noodle bowl centered on dashi aroma, thick noodle bounce, and clean warmth.",
        "taste": [("Dashi clarity", "Umami", 82), ("Noodle bounce", "Texture", 90), ("Gentle warmth", "Comfort", 78), ("Light body", "Body", 62), ("Clean finish", "Finish", 76)],
        "notes": ["Broth: dashi, soy, mirin-style sweetness", "Texture: thick, soft, springy noodles", "Aroma: scallion, fish cake, tempura", "Pairing: onigiri, tempura, green tea"],
    },
    {
        "id": "017",
        "code": "crr",
        "ko": "카레라이스",
        "en": "CURRY RICE",
        "desc": "A curry rice card for warm sauce, tender meat, potatoes, carrots, onions, and rice built for quick fullness.",
        "servings": "2 servings",
        "time": "30 min",
        "level": "Easy",
        "cost": "Est. 8,500 KRW",
        "ingredients": [("Curry roux or spice base", "2 blocks"), ("Beef, pork, or chicken", "180g"), ("Potato and carrot", "220g"), ("Onion", "1/2"), ("Rice", "2 bowls"), ("Pickles", "optional")],
        "steps": ["Brown meat and onion for depth", "Add vegetables and water, then simmer", "Melt curry base until glossy", "Serve over rice with pickles"],
        "point": "Cook onion until sweet before simmering; it gives curry a rounder base.",
        "dining": "A hearty rice plate with spiced sauce, soft vegetables, and steady warmth from first bite to finish.",
        "taste": [("Spice aroma", "Aroma", 82), ("Sauce savor", "Umami", 76), ("Mild heat", "Spice", 52), ("Hearty body", "Body", 88), ("Warm finish", "Finish", 74)],
        "notes": ["Sauce: curry roux or spice blend", "Texture: soft vegetables and rice", "Aroma: turmeric, onion, warm spices", "Pairing: pickles, salad, lassi or tea"],
    },
    {
        "id": "018",
        "code": "hbg",
        "ko": "햄버거 세트",
        "en": "BURGER SET",
        "desc": "A fast lunch card for burger, fries, drink, sauce balance, and portable takeout structure.",
        "servings": "1 set",
        "time": "7 min",
        "level": "Easy",
        "cost": "Est. 9,800 KRW",
        "ingredients": [("Burger bun", "1"), ("Beef or chicken patty", "1"), ("Cheese", "1 slice"), ("Lettuce and tomato", "1 set"), ("Fries", "1 side"), ("Drink", "1 cup")],
        "steps": ["Toast bun for structure", "Cook or warm patty and cheese", "Layer vegetables and sauce evenly", "Serve with fries and drink"],
        "point": "Sauce should support the patty without making the bun collapse.",
        "dining": "A compact fast-food set built around juicy patty, toasted bun, crisp fries, and sweet-salty balance.",
        "taste": [("Patty savor", "Umami", 82), ("Bun softness", "Texture", 68), ("Sauce tang", "Acidity", 58), ("Filling body", "Body", 86), ("Salty finish", "Finish", 70)],
        "notes": ["Base: bun, patty, cheese, vegetables", "Texture: soft bun, juicy patty, crisp fries", "Aroma: grill, sauce, fried potato", "Pairing: cola, pickles, onion rings"],
    },
    {
        "id": "019",
        "code": "dnb",
        "ko": "덮밥",
        "en": "DONBURI",
        "desc": "A Japanese rice bowl card for simmered topping, seasoned sauce, egg or beef, onion, and fast comfort.",
        "servings": "1 bowl",
        "time": "12 min",
        "level": "Easy",
        "cost": "Est. 8,000 KRW",
        "ingredients": [("Cooked rice", "1 bowl"), ("Beef or chicken", "120g"), ("Onion", "1/2"), ("Egg", "1"), ("Soy dashi sauce", "120ml"), ("Scallion", "to taste")],
        "steps": ["Simmer onion in soy dashi sauce", "Add meat until just cooked", "Pour beaten egg and set softly", "Slide topping over hot rice"],
        "point": "Stop cooking while the egg is still soft so it coats the rice.",
        "dining": "A quick rice bowl where sweet soy broth, tender topping, and soft egg soak into warm rice.",
        "taste": [("Soy dashi", "Umami", 84), ("Soft egg", "Texture", 80), ("Gentle sweetness", "Sweetness", 72), ("Rice body", "Body", 78), ("Clean finish", "Finish", 68)],
        "notes": ["Sauce: soy, dashi, mirin-style sweetness", "Texture: soft egg, tender meat, warm rice", "Aroma: onion, scallion, dashi", "Pairing: miso soup, pickles, green tea"],
    },
    {
        "id": "020",
        "code": "bnt",
        "ko": "도시락",
        "en": "HOMEMADE LUNCHBOX",
        "desc": "A meal prep card for rice or grains, protein, vegetables, fruit, and a compact cost-balanced lunch.",
        "servings": "1 box",
        "time": "20 min",
        "level": "Easy",
        "cost": "Est. 5,500 KRW",
        "ingredients": [("Rice or grain", "180g"), ("Protein main", "120g"), ("Vegetable sides", "180g"), ("Egg or tofu", "optional"), ("Fruit", "1 portion"), ("Sauce or dressing", "small cup")],
        "steps": ["Choose one grain, one protein, and two vegetables", "Cool hot items before closing the lid", "Pack sauce separately", "Keep colors and textures divided"],
        "point": "Cooling food before sealing prevents steam from making the lunchbox soggy.",
        "dining": "A planned lunch format where nutrition, cost, portion, and texture are composed into one box.",
        "taste": [("Balanced base", "Balance", 88), ("Protein focus", "Umami", 72), ("Vegetable lift", "Freshness", 82), ("Moderate body", "Body", 70), ("Clean finish", "Finish", 78)],
        "notes": ["Base: grain, protein, vegetables, fruit", "Texture: separated sections with varied bite", "Aroma: depends on main dish and sauce", "Pairing: soup cup, tea, sparkling water"],
    },
]


PRONUNCIATION = {
    "001": "kim-chee JJI-geh",
    "002": "dwen-jahng JJI-geh",
    "003": "bee-beem-bap",
    "004": "soon-doo-boo JJI-geh",
    "005": "jeh-yook BOH-kkeum",
    "006": "dohn-kka-seu",
    "007": "gook-soo",
    "008": "neng-myun",
    "009": "sahm-gyup-sahl goo-ee",
    "010": "dak-gahl-bee",
    "011": "ssahl-gook-soo",
    "012": "mah-rah-tahng",
    "013": "sal-leo-deu boh-ool",
    "014": "saen-deu-wee-chi, soo-peu",
    "015": "cho-bap and roll",
    "016": "oo-dong",
    "017": "kah-reh-rah-ee-seu",
    "018": "haem-beo-geo seh-teu",
    "019": "deop-bap",
    "020": "doh-see-rahk",
}


def font(size, bold=False):
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REG, size)


def rounded(im, radius):
    mask = Image.new("L", im.size, 0)
    d = ImageDraw.Draw(mask)
    d.rounded_rectangle((0, 0, im.size[0] - 1, im.size[1] - 1), radius=radius, fill=255)
    out = Image.new("RGBA", im.size, (0, 0, 0, 0))
    out.paste(im.convert("RGBA"), (0, 0), mask)
    return out


def fit_crop(im, size, centering=(0.5, 0.5)):
    return ImageOps.fit(im.convert("RGB"), size, method=Image.Resampling.LANCZOS, centering=centering)


def text(draw, xy, s, size, fill, bold=False, anchor=None, align="left"):
    draw.text(xy, s, font=font(size, bold), fill=fill, anchor=anchor, align=align)


def wrap(draw, s, max_w, size, bold=False):
    f = font(size, bold)
    lines = []
    for para in s.split("\n"):
        line = ""
        for word in para.split(" "):
            test = word if not line else line + " " + word
            if draw.textlength(test, font=f) <= max_w:
                line = test
            else:
                if line:
                    lines.append(line)
                line = word
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


def chip_small(draw, xy, label, color, text_color=(255, 255, 255), w=None):
    x, y = xy
    f = font(22, True)
    tw = int(draw.textlength(label, font=f))
    width = w or tw + 30
    draw.rounded_rectangle((x, y, x + width, y + 40), radius=20, fill=color)
    draw.text((x + width / 2, y + 20), label, font=f, fill=text_color, anchor="mm")
    return x + width + 10


def qr_image(url, size=150, color=(0, 0, 0)):
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=8, border=2)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color=color, back_color="white").convert("RGB")
    return img.resize((size, size), Image.Resampling.NEAREST)


def food_crop(item):
    src = Image.open(LM_SRC / f"{item['id']}_{item['code']}.png").convert("RGB")
    return src.crop((28, 350, 552, 858))


def make_recipe_en(item):
    orange = (236, 113, 33)
    deep = (144, 61, 18)
    brown = (74, 43, 24)
    im, d = card_base(orange, deep)

    text(d, (58, 51), "MaAM RECIPE", 29, (255, 242, 226), True)
    text(d, (58, 82), "LR TYPE · LINKED RECIPE", 21, (255, 228, 203), False)

    food = rounded(fit_crop(food_crop(item), (500, 360)), 28)
    im.paste(food, (48, 158), food)
    d.rounded_rectangle((48, 158, 548, 518), radius=28, outline=(228, 132, 64), width=4)

    title_size = 54 if len(item["en"]) <= 16 else 46
    text(d, (590, 160), item["en"], title_size, (24, 24, 22), True)
    text(d, (594, 224), item["ko"], 34, orange, True)
    text(d, (594, 266), "RECIPE CARD", 30, orange, True)
    multiline(d, (594, 318), item["desc"], 500, 27, brown, False, 8)

    x = 594
    y = 442
    for label, width in [(item["servings"], 142), (item["time"], 120), (item["level"], 112)]:
        x = chip_small(d, (x, y), label, orange, w=width)
    chip_small(d, (594, 490), item["cost"], orange, w=205)

    d.rounded_rectangle((48, 560, 548, 1015), radius=26, fill=(255, 244, 231), outline=(239, 178, 130), width=3)
    text(d, (80, 592), "Ingredient Checklist", 32, deep, True)
    yy = 658
    for name, amount in item["ingredients"]:
        d.ellipse((82, yy + 7, 102, yy + 27), fill=orange)
        multiline(d, (118, yy), name, 300, 22, brown, True, 2)
        text(d, (508, yy + 2), amount, 20, deep, False, anchor="ra")
        yy += 54

    d.rounded_rectangle((590, 560, 1150, 885), radius=26, fill=(255, 244, 231), outline=(239, 178, 130), width=3)
    text(d, (626, 592), "Cooking Flow", 34, deep, True)
    yy = 652
    for idx, desc in enumerate(item["steps"], 1):
        d.rounded_rectangle((626, yy, 682, yy + 42), radius=18, fill=orange)
        text(d, (654, yy + 21), f"{idx:02d}", 21, (255, 255, 255), True, anchor="mm")
        multiline(d, (702, yy + 1), desc, 405, 22, brown, False, 3)
        yy += 58

    d.rounded_rectangle((590, 920, 1150, 1198), radius=26, fill=(255, 244, 231), outline=(239, 178, 130), width=3)
    text(d, (626, 952), "Shopping Links", 34, deep, True)
    x = chip_small(d, (626, 1008), "E-Mart", (199, 80, 24), w=120)
    chip_small(d, (x, 1008), "Online Market", (199, 80, 24), w=185)
    chip_small(d, (626, 1060), "Price Compare", (199, 80, 24), w=180)
    qr = qr_image(f"maam://recipe/{item['id']}-{item['code']}?lang=en&market=emart", 150, deep)
    im.paste(qr, (952, 1026))
    text(d, (1027, 1182), "SHOP QR", 20, deep, True, anchor="mm")

    d.rounded_rectangle((48, 1050, 548, 1198), radius=26, fill=(255, 244, 231), outline=(239, 178, 130), width=3)
    text(d, (80, 1082), "Production Point", 31, deep, True)
    multiline(d, (80, 1130), item["point"], 430, 23, brown, False, 3)

    d.rounded_rectangle((30, 1233, W - 30, 1288), radius=26, fill=orange)
    text(d, (W / 2, 1261), "Cookable Food. Smart Shopping.", 25, (255, 255, 255), True, anchor="mm")
    return im


def make_fine_dining_en(item):
    purple = (122, 71, 196)
    deep = (72, 36, 128)
    ink = (35, 28, 45)
    im, d = card_base(purple, deep)

    text(d, (58, 51), "MaAM FINE DINING", 29, (246, 237, 255), True)
    text(d, (58, 82), "LF TYPE · LOCAL FINE DINING", 21, (230, 214, 255), False)

    food = rounded(fit_crop(food_crop(item), (500, 360)), 28)
    im.paste(food, (48, 158), food)
    d.rounded_rectangle((48, 158, 548, 518), radius=28, outline=(153, 116, 212), width=4)

    title_size = 54 if len(item["en"]) <= 16 else 46
    text(d, (590, 160), item["en"], title_size, (24, 24, 22), True)
    text(d, (594, 224), item["ko"], 34, purple, True)
    text(d, (594, 266), "FINE DINING NOTE", 30, purple, True)
    multiline(d, (594, 318), item["dining"], 505, 27, ink, False, 8)

    x = 594
    y = 456
    for label in ["Translate", "Restaurant", "Map", "Reserve"]:
        x = chip_small(d, (x, y), label, purple, w=126)

    d.rounded_rectangle((48, 560, 548, 1015), radius=26, fill=(248, 242, 255), outline=(178, 151, 221), width=3)
    text(d, (80, 592), "Tasting Structure", 32, deep, True)
    colors = [(130, 77, 202), (106, 87, 196), (170, 80, 162), (112, 71, 150), (99, 76, 166)]
    yy = 662
    for idx, (label, en, val) in enumerate(item["taste"]):
        text(d, (82, yy), label, 23, ink, True)
        text(d, (330, yy + 2), en, 16, (99, 87, 116), False)
        d.rounded_rectangle((82, yy + 34, 460, yy + 52), radius=9, fill=(229, 222, 241))
        d.rounded_rectangle((82, yy + 34, 82 + int(378 * val / 100), yy + 52), radius=9, fill=colors[idx % len(colors)])
        text(d, (500, yy + 44), str(val), 21, deep, True, anchor="mm")
        yy += 70

    d.rounded_rectangle((590, 560, 1150, 885), radius=26, fill=(248, 242, 255), outline=(178, 151, 221), width=3)
    text(d, (626, 592), "Dining Interpretation", 31, deep, True)
    yy = 652
    for note in item["notes"]:
        d.ellipse((626, yy + 9, 642, yy + 25), fill=purple)
        yy = multiline(d, (658, yy), note, 430, 21, ink, False, 3) + 10

    d.rounded_rectangle((48, 1050, 548, 1198), radius=26, fill=(248, 242, 255), outline=(178, 151, 221), width=3)
    text(d, (80, 1082), "How to Order", 31, deep, True)
    order_name = item["en"].lower()
    order = f'Say: "One {order_name}, please."'
    pron = f"Pronounce: {PRONUNCIATION[item['id']]}"
    multiline(d, (80, 1128), order, 430, 22, ink, False, 3)
    multiline(d, (80, 1166), pron, 430, 21, deep, True, 2)

    d.rounded_rectangle((590, 920, 1150, 1198), radius=26, fill=(248, 242, 255), outline=(178, 151, 221), width=3)
    text(d, (626, 952), "QR Service Hub", 32, deep, True)
    qr_url = "https://www.google.com/maps/search/" + quote(f"{item['en'].lower()} restaurant near me")
    qr = qr_image(qr_url, 168, deep)
    im.paste(qr, (942, 998))
    x = chip_small(d, (626, 1008), "Map Search", purple, w=130)
    chip_small(d, (x, 1008), "Translate", purple, w=130)
    chip_small(d, (626, 1058), "Reviews", purple, w=126)
    multiline(d, (626, 1142), "Scan to find nearby restaurants.", 270, 19, ink, False, 2)

    d.rounded_rectangle((30, 1233, W - 30, 1288), radius=26, fill=purple)
    text(d, (W / 2, 1261), "Taste Beyond Menu. Search Beyond Card.", 25, (255, 255, 255), True, anchor="mm")
    return im


def save_cards():
    recipe_out = OUT / "recipe"
    fine_out = OUT / "fine_dining"
    recipe_asset = ASSET_CARD / "lr-card"
    fine_asset = ASSET_CARD / "lf-card"
    recipe_out.mkdir(parents=True, exist_ok=True)
    fine_out.mkdir(parents=True, exist_ok=True)
    recipe_asset.mkdir(parents=True, exist_ok=True)
    fine_asset.mkdir(parents=True, exist_ok=True)

    saved = []
    for item in MENU:
        lr = make_recipe_en(item)
        lf = make_fine_dining_en(item)
        lr_name = f"{item['id']}_{item['code']}_lr.png"
        lf_name = f"{item['id']}_{item['code']}_lf.png"
        lr_path = recipe_out / lr_name
        lf_path = fine_out / lf_name
        lr.save(lr_path, quality=95)
        lf.save(lf_path, quality=95)
        lr.save(recipe_asset / lr_name, quality=95)
        lf.save(fine_asset / lf_name, quality=95)
        saved.extend([lr_path, lf_path, recipe_asset / lr_name, fine_asset / lf_name])
    return saved


def save_one(item_id):
    item = next(item for item in MENU if item["id"] == item_id)
    fine_out = OUT / "fine_dining"
    fine_asset = ASSET_CARD / "lf-card"
    fine_out.mkdir(parents=True, exist_ok=True)
    fine_asset.mkdir(parents=True, exist_ok=True)
    lf = make_fine_dining_en(item)
    lf_name = f"{item['id']}_{item['code']}_lf.png"
    paths = [fine_out / lf_name, fine_asset / lf_name]
    for path in paths:
        lf.save(path, quality=95)
    return paths


if __name__ == "__main__":
    for path in save_cards():
        print(path)
