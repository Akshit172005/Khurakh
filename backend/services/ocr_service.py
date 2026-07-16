import easyocr
import cv2
import re

reader = easyocr.Reader(['en'], gpu=False)

REMOVE_WORDS = {
    "tablet","tablets","capsule","capsules","mg","ml",
    "manufactured","batch","expiry","exp","mrp",
    "cipla","sun","pharma","adystra","ltd","india",
    "strip","pack","ip","usp"
}

def extract_text(image_path):

    image = cv2.imread(image_path)

    if image is None:
        return ""

    results = reader.readtext(image)

    candidates = []

    print("\n========== EASY OCR ==========")

    for _, text, conf in results:

        print(text, conf)

        if conf < 0.25:
            continue

        text = re.sub(r"[^A-Za-z0-9 ]", "", text).strip()

        if len(text) < 3:
            continue

        lower = text.lower()

        if lower in REMOVE_WORDS:
            continue

        if any(char.isdigit() for char in text):
            continue

        candidates.append(text)

    print("==============================")

    # remove duplicates
    seen = set()
    final = []

    for word in candidates:
        if word.lower() not in seen:
            seen.add(word.lower())
            final.append(word)

    medicine = " ".join(final[:2])

    print("\nFINAL MEDICINE:")
    print(medicine)

    return medicine