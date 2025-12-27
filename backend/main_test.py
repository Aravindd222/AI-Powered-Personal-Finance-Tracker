from ocr_engine import extract_ocr_blocks
from parser_ml import extract_amount_strict, detect_category_ml,extract_date

IMAGE = "snookers.png"

blocks = extract_ocr_blocks(IMAGE)

amount = extract_amount_strict(blocks)
category = detect_category_ml(blocks)

print("FINAL AMOUNT:", amount)
print("CATEGORY:", category["category"])
print("SUB CATEGORY:", category["subcategory"])
print("DATE:", extract_date(blocks))
