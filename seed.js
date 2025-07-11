const mongoose = require('mongoose');
const fs = require('fs');
const csv = require('csv-parser');
const Barcode = require('./models/barcode');

mongoose.connect('mongodb://localhost:27017/BarcodeDB')
  .then(() => {
    console.log("✅ Connected to MongoDB");
    seedData();
  })
  .catch(err => {
    console.error("❌ MongoDB connection error:", err);
  });

function seedData() {
  const records = [];

  fs.createReadStream('C:/Users/R3/Downloads/barcode-lookup-server/pcb_traceability_labeled_dataset.csv')
    .pipe(csv())
    .on('data', (row) => {
      records.push({
        barcode: row.barcode.trim(), // ✅ Store as string
        batch_id: row.batch_id,
        shift_id: row.shift_id,
        place_id: row.place_id,
        manufacturing_date: row.manufacturing_date,
        quality_status: row.quality_status,
        defect_type: row.defect_type,
        operator_id: row.operator_id,
        operator_name: row.operator_name,
        timestamp: row.timestamp,
        product_id: row.product_id,
        last_scanned_at: null
      });
    })
    .on('end', async () => {
      try {
        await Barcode.deleteMany();
        await Barcode.insertMany(records);
        console.log(`✅ Inserted ${records.length} records`);
        mongoose.disconnect();
      } catch (err) {
        console.error("❌ Error inserting data:", err);
      }
    })
    .on('error', (err) => {
      console.error("❌ CSV Read Error:", err);
    });
}
