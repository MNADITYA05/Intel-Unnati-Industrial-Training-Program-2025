// server.js
const express = require('express');
const mongoose = require('mongoose');
const bodyParser = require('body-parser');
const Barcode = require('./models/barcode');
const axios = require('axios');

console.log("🛠 server.js started");

mongoose.connect('mongodb://localhost:27017/BarcodeDB')
  .then(() => console.log("✅ Connected to MongoDB"))
  .catch(err => console.error("❌ MongoDB connection error:", err));

const app = express();
app.use(bodyParser.json());

app.get('/', (req, res) => {
  res.send("🔄 Barcode Lookup Server is Running");
});

app.post('/lookup', async (req, res) => {
  let { barcode } = req.body;

  // 🧼 Sanitize barcode input
  barcode = String(barcode).trim().replace(/\s/g, '').replace(/[\u200B-\u200D\uFEFF]/g, '');

  console.log("📥 Received barcode:", barcode);

  if (!barcode || typeof barcode !== 'string' || barcode.length !== 13) {
    return res.status(400).json({ status: "error", message: "Barcode must be a 13-digit string" });
  }

  try {
    const record = await Barcode.findOneAndUpdate(
      { barcode },
      { last_scanned_at: new Date().toISOString() },
      { new: true }
    );

    if (record) {
      console.log("✅ Found:", record);

      // Trigger ML API
      try {
        const response = await axios.post("http://localhost:8000/trigger", {
          product_id: record.product_id
        });

        console.log("📦 ML API response:", response.data);

        return res.json({
          status: "found",
          barcode: record.barcode,
          product_id: record.product_id,
          manufacturing_date: record.manufacturing_date,
          ml_result: response.data
        });
      } catch (mlError) {
        console.error("❌ ML API trigger failed:", mlError.message);
        return res.status(500).json({ status: "ml_error", message: "ML API trigger failed" });
      }
    } else {
      console.warn("❌ Not found in DB:", barcode);
      return res.status(404).json({ status: "not_found", message: "Barcode not found" });
    }
  } catch (err) {
    console.error("❌ Lookup failed:", err);
    return res.status(500).json({ status: "error", message: "Internal server error" });
  }
});

const PORT = process.env.PORT || 5050;
app.listen(PORT, '0.0.0.0', () => {
  console.log(`🚀 Server running on http://localhost:${PORT}`);
});
