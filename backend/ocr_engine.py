import easyocr

reader = easyocr.Reader(['en'])

def extract_ocr_blocks(image_path):
    """
    Returns OCR blocks in a standard format:
    {
      text: str,
      box: [[x,y] * 4],
      conf: float
    }
    """
    results = reader.readtext(image_path)

    blocks = []
    for box, text, conf in results:
        blocks.append({
            "text": text,
            "box": box,
            "conf": conf
        })

    return blocks


def extract_plain_text(ocr_blocks):
    return " ".join(b["text"] for b in ocr_blocks)
