# ml_api.py

from fastapi import FastAPI
from pydantic import BaseModel
from ml_core import process_image
import os
import glob

app = FastAPI()  # ✅ THIS MUST EXIST

IMAGE_DIR = "pcb_with_barcodes"

class TriggerInput(BaseModel):
    product_id: str

@app.post("/trigger")
def trigger_detection(input: TriggerInput):
    search_pattern = os.path.join(IMAGE_DIR, f"*_{input.product_id}.png")
    matches = glob.glob(search_pattern)

    if not matches:
        return {"success": False, "reason": "Image not found for product_id"}

    image_path = matches[0]
    result = process_image(image_path)
    return result
