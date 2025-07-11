import streamlit as st
import cv2
import numpy as np
import os
from pymongo import MongoClient
from ultralytics import YOLO
from PIL import Image
from pyzbar.pyzbar import decode
import time

# ------------------------ CONFIG ------------------------
st.set_page_config(page_title="PCB Defect Detection", layout="wide", page_icon="🤖")
st.markdown("<h3 style='text-align: center;'>🔍 Fast PCB Defect Detection with YOLO & Barcode Decoder</h3>", unsafe_allow_html=True)

DEFAULT_IMAGE_FOLDER = r"C:\Users\R3\Downloads\barcode-lookup-server\pcb_with_barcodes"

# ------------------------ MongoDB ------------------------
@st.cache_resource
def get_collection():
    client = MongoClient("mongodb://localhost:27017")
    db = client["BarcodeDB"]
    return db["barcodes"]

collection = get_collection()

# ------------------------ YOLO ------------------------
@st.cache_resource
def load_yolo_model():
    try:
        return YOLO("best.pt")
    except Exception as e:
        st.error(f"❌ Failed to load YOLO model: {e}")
        st.stop()

yolo_model = load_yolo_model()

# ------------------------ Utility Functions ------------------------
def extract_barcode_from_image_pyzbar(image_pil):
    decoded_objects = decode(image_pil)
    for obj in decoded_objects:
        barcode_data = obj.data.decode("utf-8").strip()
        if len(barcode_data) == 13 and barcode_data.isdigit():
            return barcode_data
    return None

def mask_barcode_area(image_rgb):
    decoded_objects = decode(Image.fromarray(image_rgb))
    for obj in decoded_objects:
        points = obj.polygon
        if points:
            pts = np.array([[p.x, p.y] for p in points], np.int32)
            cv2.fillPoly(image_rgb, [pts], (255, 255, 255))
    return image_rgb

def detect_defects_with_yolo(image, conf_thresh=0.25):
    results = yolo_model.predict(source=image, conf=conf_thresh, verbose=False)
    result = results[0]
    annotated_img = result.plot()
    defects = []
    boxes = result.boxes
    if boxes is not None:
        for box in boxes:
            class_id = int(box.cls[0])
            confidence = float(box.conf[0])
            class_name = yolo_model.names[class_id]
            defects.append({"type": class_name, "confidence": confidence})
    return annotated_img, defects

def update_db(barcode, defects):
    defect_types = [d["type"] for d in defects]
    quality_status = "defective" if defect_types else "no_defect"
    defect_type_str = ", ".join(defect_types) if defect_types else "none"

    result = collection.update_one(
        {"barcode": barcode},
        {"$set": {
            "quality_status": quality_status,
            "defect_type": defect_type_str
        }},
    )
    return result

# ------------------------ Streamlit UI ------------------------
def main():
    conf_thresh = 0.25

    if not os.path.exists(DEFAULT_IMAGE_FOLDER):
        st.error(f"📁 Folder not found: {DEFAULT_IMAGE_FOLDER}")
        return

    image_files = [f for f in os.listdir(DEFAULT_IMAGE_FOLDER) if f.lower().endswith((".png", ".jpg", ".jpeg"))]

    if not image_files:
        st.warning("⚠️ No image files found in folder.")
        return

    with st.sidebar:
        st.caption("📂 *Select PCB Image*")
        selected_image = st.selectbox("Choose Image", image_files)

    if not selected_image:
        st.info("🖼️ Please select an image to begin.")
        return

    image_path = os.path.join(DEFAULT_IMAGE_FOLDER, selected_image)
    image = cv2.imread(image_path)
    if image is None:
        st.error("❌ Failed to read the image.")
        return

    h, w, _ = image.shape
    if max(h, w) > 400:
        scale = 400 / max(h, w)
        image = cv2.resize(image, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_AREA)

    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_pil = Image.fromarray(image_rgb)
    masked_image_rgb = mask_barcode_area(image_rgb.copy())

    col1, col2 = st.columns(2)
    with col1:
        st.image(image_rgb, caption="📷 Input Image", use_column_width=True)

    with col2:
        with st.spinner("🛠 Running YOLO Defect Detection..."):
            start_time = time.time()
            result_image, defects = detect_defects_with_yolo(masked_image_rgb, conf_thresh)
            elapsed = time.time() - start_time
        st.image(result_image[..., ::-1], caption="📌 YOLO Detection Result", use_column_width=True)

    st.success(f"✅ YOLO Completed in {elapsed:.2f} sec")
    st.markdown("---")

    col_barcode, col_defects, col_update = st.columns(3)

    with col_barcode:
        with st.spinner("🔎 Extracting barcode..."):
            barcode = extract_barcode_from_image_pyzbar(image_pil)
        if barcode:
            st.info(f"📦 *Barcode:* `{barcode}`")
        else:
            st.error("❌ Could not extract 13-digit barcode.")
            return

    with col_defects:
        st.subheader("🛠 Defects")
        if defects:
            for d in defects:
                st.write(f"- `{d['type']}` | Conf: `{d['confidence']:.2f}`")
        else:
            st.success("✅ No defects detected.")

    with col_update:
        if st.button("📥 Update in DB", use_container_width=True):
            result = update_db(barcode, defects)
            if result.matched_count == 0:
                st.error("❌ Update failed: Barcode not found.")
            elif result.modified_count > 0:
                st.success("✅ DB updated successfully.")
            else:
                st.info("ℹ Already up to date.")
            updated_doc = collection.find_one({"barcode": barcode})
            if updated_doc:
                with st.expander("📄 Document After Update", expanded=False):
                    st.json(updated_doc)

if __name__ == "__main__":
    main()
