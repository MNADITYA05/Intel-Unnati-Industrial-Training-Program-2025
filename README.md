# Intel-Unnati-Industrial-Training-Program-2025


## System Architecture Overview

This smart automated product labeling and traceability system implements a comprehensive workflow that combines hardware scanning, database verification, and AI-powered quality inspection to ensure product authenticity and quality control. The system begins with an ESP32 microcontroller equipped with barcode scanning capabilities, which captures product identifiers and initiates the verification process.

When a barcode is scanned, the ESP32 transmits the data via HTTP POST request to a Node.js server (server.js), which serves as the central orchestrator for the entire workflow. The server immediately queries a MongoDB database using predefined schemas (models/barcode.js) to verify whether the scanned product exists in the system's inventory records. This initial verification step ensures that only registered products proceed through the quality assessment pipeline.

For validated products, the system triggers an advanced machine learning pipeline through ml_api.py, which coordinates with ml_core.py to perform comprehensive image analysis. The process_image() function simultaneously handles multiple critical tasks: loading the product image, extracting barcode information for cross-verification, and applying masking techniques to isolate relevant inspection areas. The core quality assessment utilizes a pre-trained YOLOv11n model (best.pt) to detect potential defects and calculate confidence scores, providing quantitative metrics for product quality evaluation.

The AI inspection results, including defect classifications and confidence levels, are automatically logged back to the MongoDB database, updating the product record with real-time quality_status and defect_type information. This creates a permanent audit trail for traceability purposes. Finally, the complete inspection results are transmitted back through the server.js to the ESP32, where comprehensive product information and quality status are displayed on an integrated TFT screen, providing immediate feedback to operators and ensuring transparency in the quality control process.

This architecture enables real-time product authentication, automated quality inspection, and comprehensive traceability tracking, making it ideal for manufacturing environments, supply chain management, and quality assurance applications where product integrity and documentation are critical requirements.


![WhatsApp Image 2025-07-05 at 03 14 45_629258ff](https://github.com/user-attachments/assets/18fb775a-fd9b-4954-9f8c-a846f95eee53)

![CONFUSION MATRIX.jpeg](https://github.com/MNADITYA05/Intel-Unnati-Industrial-Training-Program-2025/blob/main/ASSETS/CONFUSION%20MATRIX.jpeg)

![TRAINING RESULTS.jpeg](https://github.com/MNADITYA05/Intel-Unnati-Industrial-Training-Program-2025/blob/main/ASSETS/TRAINING%20RESULTS.jpeg)

![TEST OUTPUT.jpeg](https://github.com/MNADITYA05/Intel-Unnati-Industrial-Training-Program-2025/blob/main/ASSETS/TEST%20OUTPUT.jpeg)



