from pymongo import MongoClient
from pyzbar.pyzbar import decode
from PIL import Image
from ultralytics import YOLO
import numpy as np
import cv2
from datetime import datetime

# Load YOLO model
model = YOLO("best.pt")

# MongoDB connection
client = MongoClient("mongodb://localhost:27017")
collection = client["BarcodeDB"]["barcode"]

def extract_barcode(image_pil):
    for obj in decode(image_pil):
        text = obj.data.decode("utf-8").strip()
        if text.isdigit() and len(text) == 13:
            return text
    return None

def mask_barcode(image_rgb):
    for obj in decode(Image.fromarray(image_rgb)):
        points = obj.polygon
        if points:
            pts = np.array([[p.x, p.y] for p in points], np.int32)
            cv2.fillPoly(image_rgb, [pts], (255, 255, 255))
    return image_rgb

def detect_defects(image_rgb):
    results = model.predict(source=image_rgb, conf=0.25, verbose=False)[0]
    defects = []
    if results.boxes:
        for box in results.boxes:
            class_id = int(box.cls[0])
            confidence = float(box.conf[0])
            class_name = model.names[class_id]
            defects.append({"type": class_name, "confidence": confidence})
    return defects

def update_barcode(barcode_val, defects):
    quality = "defective" if defects else "no_defect"
    defect_str = ", ".join([d["type"] for d in defects]) or "none"

    result = collection.update_one(
        { "barcode": str(barcode_val) },
        { "$set": {
            "quality_status": quality,
            "defect_type": defect_str,
            "last_updated": datetime.utcnow().isoformat()
        }}
    )

    return result.modified_count > 0

def process_image(image_path):
    image = cv2.imread(image_path)
    if image is None:
        return {"success": False, "reason": "Image read failed"}

    # Resize if too large (similar to ml.py)
    h, w, _ = image.shape
    if max(h, w) > 400:
        scale = 400 / max(h, w)
        image = cv2.resize(image, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_AREA)

    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_pil = Image.fromarray(image_rgb)

    barcode = extract_barcode(image_pil)
    if not barcode:
        return {"success": False, "reason": "OCR failed (barcode not found)"}

    masked = mask_barcode(image_rgb.copy())
    defects = detect_defects(masked)
    updated = update_barcode(barcode, defects)

    return {
        "success": True,
        "barcode": barcode,
        "quality_status": "defective" if defects else "no_defect",
        "defect_type": [d["type"] for d in defects] or ["none"],
        "updated": updated
    }
