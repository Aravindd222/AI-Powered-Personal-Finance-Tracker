import easyocr
import numpy as np
import cv2


def extract_ocr_blocks(image_bytes):
    reader = easyocr.Reader(['en'])
    """
    Accepts image bytes and returns OCR blocks in standard format:
    {
      text: str,
      box: [[x,y] * 4],
      conf: float
    }
    """

    # Convert bytes → numpy array
    np_arr = np.frombuffer(image_bytes, np.uint8)

    # Decode image
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    if img is None:
        raise ValueError("Invalid image file")

    results = reader.readtext(img)

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
