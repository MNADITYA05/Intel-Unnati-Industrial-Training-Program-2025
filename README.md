# Intel-Unnati-Industrial-Training-Program-2025

![FLOW MAP.jpeg](https://github.com/MNADITYA05/Intel-Unnati-Industrial-Training-Program-2025/blob/main/ASSETS/FLOW%20MAP.jpeg)

## System Architecture Overview

This smart automated product labeling and traceability system implements a comprehensive workflow that combines hardware scanning, database verification, and AI-powered quality inspection to ensure product authenticity and quality control. The system begins with an ESP32 microcontroller equipped with barcode scanning capabilities, which captures product identifiers and initiates the verification process.

When a barcode is scanned, the ESP32 transmits the data via HTTP POST request to a Node.js server (server.js), which serves as the central orchestrator for the entire workflow. The server immediately queries a MongoDB database using predefined schemas (models/barcode.js) to verify whether the scanned product exists in the system's inventory records. This initial verification step ensures that only registered products proceed through the quality assessment pipeline.

For validated products, the system triggers an advanced machine learning pipeline through ml_api.py, which coordinates with ml_core.py to perform comprehensive image analysis. The process_image() function simultaneously handles multiple critical tasks: loading the product image, extracting barcode information for cross-verification, and applying masking techniques to isolate relevant inspection areas. The core quality assessment utilizes a pre-trained YOLOv11n model (best.pt) to detect potential defects and calculate confidence scores, providing quantitative metrics for product quality evaluation.

The AI inspection results, including defect classifications and confidence levels, are automatically logged back to the MongoDB database, updating the product record with real-time quality_status and defect_type information. This creates a permanent audit trail for traceability purposes. Finally, the complete inspection results are transmitted back through the server.js to the ESP32, where comprehensive product information and quality status are displayed on an integrated TFT screen, providing immediate feedback to operators and ensuring transparency in the quality control process.

This architecture enables real-time product authentication, automated quality inspection, and comprehensive traceability tracking, making it ideal for manufacturing environments, supply chain management, and quality assurance applications where product integrity and documentation are critical requirements.


![WhatsApp Image 2025-07-05 at 03 14 45_629258ff](https://github.com/user-attachments/assets/18fb775a-fd9b-4954-9f8c-a846f95eee53)

## Hardware Implementation

This image showcases the physical implementation of the smart automated product labeling and traceability system, demonstrating the seamless integration of embedded hardware components that bring the workflow architecture to life. At the center of the system is an ESP32-WROOM-32 development board, which serves as the primary microcontroller responsible for orchestrating all hardware interactions and maintaining connectivity with the backend infrastructure.

The system features a high-resolution TFT display that provides real-time feedback to operators, as evidenced by the current screen showing a "MATCHED" status for a successfully verified product. The display presents comprehensive product information including the unique product identifier (A4BNW10020001), manufacturing date (01-06-2023), barcode number (1100100200013), and critically, the AI-determined quality assessment result showing "defective" status. This immediate visual feedback ensures operators can quickly identify product status without requiring additional verification steps.

A compact camera module positioned strategically within the system enables automated image capture for the machine learning pipeline. This camera works in conjunction with the ESP32 to photograph products during the scanning process, providing the visual data necessary for the YOLOv8 defect detection algorithm. The camera's integration allows for hands-free operation where products can be placed in the scanning area and automatically photographed for analysis.

The color-coded wiring system demonstrates the organized approach to component integration, with dedicated connections for power distribution, data communication, and display control. The ESP32's Wi-Fi capabilities enable seamless communication with the Node.js server infrastructure, allowing real-time data exchange between the physical scanning station and the cloud-based verification and AI analysis systems.

This hardware configuration creates a complete scanning workstation that combines barcode reading capabilities, visual inspection through AI-powered image analysis, database verification, and immediate result display. The compact form factor makes it suitable for integration into existing production lines, quality control stations, or warehouse management systems, while the modular design allows for easy maintenance and potential upgrades to individual components as technology evolves.


![CONFUSION MATRIX.jpeg](https://github.com/MNADITYA05/Intel-Unnati-Industrial-Training-Program-2025/blob/main/ASSETS/CONFUSION%20MATRIX.jpeg)

![TRAINING RESULTS.jpeg](https://github.com/MNADITYA05/Intel-Unnati-Industrial-Training-Program-2025/blob/main/ASSETS/TRAINING%20RESULTS.jpeg)

![TEST OUTPUT.jpeg](https://github.com/MNADITYA05/Intel-Unnati-Industrial-Training-Program-2025/blob/main/ASSETS/TEST%20OUTPUT.jpeg)

## AI Model Performance and Validation

The machine learning component of the smart automated product labeling and traceability system demonstrates exceptional performance in detecting and classifying product defects, as evidenced by comprehensive model validation metrics and real-world testing results. The system employs a specialized YOLOv8 model trained specifically for identifying various types of manufacturing defects in printed circuit boards and electronic components.

The confusion matrix reveals the model's robust classification capabilities across seven distinct defect categories: missing holes, mouse bites, open circuits, shorts, spurs, spurious copper formations, and background elements. The diagonal dominance in the matrix indicates high accuracy rates, with the model achieving over 90% correct classification for most defect types. Particularly noteworthy is the model's ability to distinguish between similar defect patterns, such as differentiating shorts from open circuits, which is critical for accurate quality assessment in the production environment.

The visual validation demonstrates the precision of the defect detection system through side-by-side comparison of original PCB images, ground truth annotations, model predictions, and combined overlays. The model successfully identifies and localizes defects with remarkable spatial accuracy, as shown by the close alignment between predicted bounding boxes (red) and actual defect locations (green). This pixel-level precision ensures that the system can reliably flag defective products while minimizing false positives that could disrupt production workflows.

The comprehensive training results showcase the model's learning progression across 100 epochs, with all loss functions (box localization, classification, and distribution focal loss) converging to optimal values. The validation metrics demonstrate consistent performance with precision reaching 95%, recall achieving 90%, and mean Average Precision (mAP) scores exceeding 85% at IoU thresholds of 0.5 and 0.5-0.95. These metrics confirm that the model maintains high accuracy on unseen data, ensuring reliable performance when deployed in the production environment.

This AI-powered defect detection system forms the core intelligence of the quality assessment pipeline, enabling automated decision-making that integrates seamlessly with the barcode verification and traceability database. The combination of high accuracy, precise localization, and robust classification capabilities ensures that the system can maintain stringent quality standards while supporting high-throughput manufacturing operations.

**DEMO**

https://drive.google.com/drive/u/1/folders/1wrUGtJpEzwsIgXT9DZ-llEh-kEH1NKC5
https://drive.google.com/file/d/1WZgZbUF2lxWeafZvHo3Jk_6ksEE0DptM/view?usp=sharing




