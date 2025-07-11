import streamlit as st
import pandas as pd
from pymongo import MongoClient
from datetime import datetime

# ------------------------ CONFIG ------------------------
st.set_page_config(page_title="Live PCB Scan Monitor", layout="wide", page_icon="📡")
st.markdown("<h2 style='text-align: center;'>📊 Real-Time PCB Scan Monitoring</h2>", unsafe_allow_html=True)

# ------------------------ MongoDB ------------------------
@st.cache_resource
def get_collection():
    client = MongoClient("mongodb://localhost:27017")
    db = client["BarcodeDB"]
    return db["barcode"]

collection = get_collection()

# ------------------------ UI ------------------------
with st.sidebar:
    st.header("🔎 Filters")
    shift_filter = st.selectbox("Shift", ["All", "A", "B", "C"])
    quality_filter = st.selectbox("Quality Status", ["All", "defective", "no_defect"])
    defect_filter = st.text_input("Search Defect Type (partial match)")

# ------------------------ Query & Display ------------------------
query = {}
if shift_filter != "All":
    query["shift_id"] = shift_filter
if quality_filter != "All":
    query["quality_status"] = quality_filter
if defect_filter:
    query["defect_type"] = {"$regex": defect_filter, "$options": "i"}

docs = list(collection.find(query).sort("last_updated", -1).limit(50))

if docs:
    df = pd.DataFrame(docs)
    df["last_updated"] = pd.to_datetime(df["last_updated"])
    df = df[["barcode", "product_id", "shift_id", "quality_status", "defect_type", "last_updated"]]
    st.dataframe(df, use_container_width=True, height=600)
else:
    st.info("No records match the filters.")

# ------------------------ Summary Stats ------------------------
st.markdown("---")
st.subheader("📈 Summary Statistics")

total = collection.count_documents({})
defect_count = collection.count_documents({"quality_status": "defective"})
no_defect_count = collection.count_documents({"quality_status": "no_defect"})

col1, col2, col3 = st.columns(3)
col1.metric("Total Scans", total)
col2.metric("Defective", defect_count)
col3.metric("OK", no_defect_count)
