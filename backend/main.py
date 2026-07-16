from services.ocr_service import extract_text

print("🚀 Starting DawaiCheck...")

image_path = "../test_images/med1.jpg"

text = extract_text(image_path)

print("\n🔍 Extracted Text:\n")
print(text)