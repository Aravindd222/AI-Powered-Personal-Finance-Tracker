from ocr_engine import extract_ocr_blocks
from parser_ml import extract_amount_strict, detect_category_ml

IMAGE = "gas.jpg"

blocks = extract_ocr_blocks(IMAGE)

amount = extract_amount_strict(blocks)
category = detect_category_ml(blocks)

print("FINAL AMOUNT:", amount)
print("CATEGORY:", category["category"])
print("SUB CATEGORY:", category["subcategory"])
