# 🎯 Stock Opname Monitoring System
## Deep Learning untuk Otomasi Manajemen Inventori

**Project ID:** DB8-PI041  
**Author:** Ivan David (B25B8M113)  
**Bootcamp:** Dicoding - Machine Learning Capstone Project

---

## 📋 Deskripsi Project

Project ini mengintegrasikan **Object Detection** dan **Time Series Forecasting** untuk menciptakan sistem monitoring stok barang otomatis di lingkungan retail. Sistem dapat:

1. 🔍 Mendeteksi dan menghitung produk di rak menggunakan Computer Vision
2. 📈 Memprediksi tren stok dan waktu kekosongan dengan Time Series
3. 🌐 Menyediakan interface web untuk monitoring real-time

---

## 🚀 Quick Start Guide

### **Langkah 1: Setup Environment**

```bash
# Clone repository (atau download project)
git clone [your-repo-url]
cd stock-opname-monitoring

# Buat virtual environment
python -m venv venv

# Aktifkan virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### **Langkah 2: Download SKU-110K Dataset**

#### **Opsi A: Download Manual (Recommended)**

1. **Download Images:**
   - Kunjungi: https://drive.google.com/file/d/1iq93lCdhaPUN0fhbJmBu6FP2-FpGp0kp/view
   - Download file: `SKU110K_fixed.tar.gz` (~13GB)
   - Extract ke folder `data/SKU110K/`

2. **Download Annotations:**
   - Kunjungi: https://github.com/eg4000/SKU110K_CVPR19
   - Download folder `annotations/`
   - Letakkan di `data/SKU110K/annotations/`

#### **Opsi B: Kaggle (Alternative)**

```bash
# Install Kaggle CLI
pip install kaggle

# Setup Kaggle API credentials (ikuti: https://www.kaggle.com/docs/api)

# Download dataset
kaggle datasets download -d thedagger/sku110k-annotations
unzip sku110k-annotations.zip -d data/SKU110K/
```

#### **Verifikasi Dataset:**

```bash
# Jalankan setup script
python setup_dataset.py

# Jika sudah manual download:
python setup_dataset.py --skip-download
```

**Struktur Folder yang Diharapkan:**
```
data/
└── SKU110K/
    ├── images/
    │   ├── train/
    │   ├── val/
    │   └── test/
    └── annotations/
        ├── annotations_train.csv
        ├── annotations_val.csv
        └── annotations_test.csv
```

### **Langkah 3: Eksplorasi Dataset**

```bash
# Jalankan Jupyter notebook
jupyter notebook

# Buka: 01_data_exploration.ipynb
# Run semua cells untuk eksplorasi dataset
```

**Yang akan Anda lihat:**
- ✅ Statistik dataset (jumlah images, objects, dll)
- ✅ Distribusi objek per image
- ✅ Analisis bounding box
- ✅ Visualisasi sample images dengan deteksi

---

## 📊 Dataset Information

### **SKU-110K Dataset**

Dataset dense object detection yang berisi gambar rak retail dengan produk-produk yang berdekatan.

| Metric | Value |
|--------|-------|
| Total Images | ~11,760 images |
| Training Set | ~8,200 images |
| Validation Set | ~580 images |
| Test Set | ~2,940 images |
| Total Objects | ~1.7 million |
| Avg Objects/Image | ~147 objects |
| Object Type | Retail products on shelves |

**Karakteristik:**
- Dense annotations (banyak objek per image)
- Small objects (produk retail)
- Varying lighting conditions
- Real-world retail scenarios

---

## 🛠️ Tech Stack

### **Machine Learning:**
- **Object Detection:** YOLOv8 / Faster R-CNN
- **Time Series:** LSTM / TCN
- **Framework:** TensorFlow, Keras, PyTorch

### **Backend:**
- **API:** Flask / Django
- **Data Processing:** NumPy, Pandas

### **Frontend:**
- **Framework:** Streamlit (MVP) / React (Production)
- **Visualization:** Matplotlib, Plotly, Chart.js

### **Development:**
- **IDE:** Jupyter Notebook, VS Code
- **Version Control:** Git, GitHub

---

## 📁 Project Structure

```
stock-opname-monitoring/
├── data/
│   └── SKU110K/                    # Dataset folder
│       ├── images/
│       └── annotations/
│
├── notebooks/
│   ├── 01_data_exploration.ipynb   # ✓ Eksplorasi dataset
│   ├── 02_preprocessing.ipynb      # Data preprocessing
│   ├── 03_yolov8_training.ipynb    # Training object detection
│   ├── 04_timeseries_model.ipynb   # Time series forecasting
│   └── 05_integration.ipynb        # Integrasi kedua model
│
├── src/
│   ├── models/
│   │   ├── object_detection.py     # Object detection module
│   │   └── time_series.py          # Time series module
│   ├── utils/
│   │   ├── preprocessing.py        # Data preprocessing utils
│   │   └── visualization.py        # Visualization utils
│   └── app/
│       ├── backend/                # Flask API
│       └── frontend/               # Streamlit/React UI
│
├── weights/                        # Trained model weights
├── results/                        # Training results & logs
├── docs/                           # Documentation
│
├── requirements.txt                # ✓ Dependencies
├── setup_dataset.py                # ✓ Dataset setup script
└── README.md                       # ✓ This file
```

---

## 🎯 Development Roadmap

### **Phase 1: Dataset & Exploration (Week 1-2)** ✅ YOU ARE HERE

- [x] Setup environment
- [x] Download SKU-110K dataset
- [x] Create exploration notebook
- [ ] Run data exploration
- [ ] Analyze dataset statistics

### **Phase 2: Object Detection (Week 2-3)**

- [ ] Data preprocessing & augmentation
- [ ] Setup YOLOv8
- [ ] Train with pretrained weights
- [ ] Evaluate on validation set
- [ ] Optimize hyperparameters

### **Phase 3: Time Series Forecasting (Week 3-4)**

- [ ] Generate/collect stock time series data
- [ ] Build LSTM/TCN model
- [ ] Train forecasting model
- [ ] Validate predictions
- [ ] Integration with detection results

### **Phase 4: Web Application (Week 4-5)**

- [ ] Design system architecture
- [ ] Build Flask backend API
- [ ] Create Streamlit frontend
- [ ] Integration testing
- [ ] UI/UX improvements

### **Phase 5: Testing & Deployment (Week 5-6)**

- [ ] End-to-end testing
- [ ] Performance optimization
- [ ] Documentation
- [ ] Deployment setup
- [ ] Final presentation

---

## 📝 Next Steps (Setelah Eksplorasi Dataset)

1. **Run Exploration Notebook:**
   ```bash
   jupyter notebook 01_data_exploration.ipynb
   ```

2. **Analisis hasil eksplorasi:**
   - Review dataset statistics
   - Identify potential challenges
   - Plan preprocessing strategy

3. **Preprocessing (Next notebook):**
   - Resize images (640x640)
   - Data augmentation
   - Train/val split verification
   - Convert to YOLO format

4. **Start YOLOv8 Training:**
   - Install Ultralytics
   - Load pretrained weights
   - Fine-tune on SKU-110K
   - Monitor training metrics

---

## 🔧 Troubleshooting

### **Dataset Download Issues:**

**Problem:** Google Drive download limit
**Solution:** 
- Gunakan akun Google lain
- Download in parts
- Atau gunakan Kaggle alternative

### **Memory Issues:**

**Problem:** Out of memory during training
**Solution:**
- Reduce batch size
- Use smaller image size (416x416)
- Use pretrained model (less memory)
- Enable mixed precision training

### **GPU Not Available:**

**Problem:** No GPU for training
**Solution:**
- Use Google Colab (free GPU)
- Use Kaggle Notebooks
- Reduce model size (YOLOv8n instead of YOLOv8x)
- Train on subset of data

---

## 📚 Resources & References

### **Papers:**
- SKU-110K Dataset: [CVPR 2019](https://arxiv.org/abs/1904.00853)
- YOLOv8: [Ultralytics Documentation](https://docs.ultralytics.com/)
- Faster R-CNN: [arXiv:1506.01497](https://arxiv.org/abs/1506.01497)
- TCN: [arXiv:1803.01271](https://arxiv.org/abs/1803.01271)

### **Tutorials:**
- [YOLOv8 Training Guide](https://docs.ultralytics.com/modes/train/)
- [Time Series with LSTM](https://www.tensorflow.org/tutorials/structured_data/time_series)
- [Flask API Development](https://flask.palletsprojects.com/)

### **Tools:**
- [Roboflow](https://roboflow.com/) - Dataset preprocessing
- [Weights & Biases](https://wandb.ai/) - Experiment tracking
- [TensorBoard](https://www.tensorflow.org/tensorboard) - Training visualization

---

## 🤝 Contributing

Ini adalah capstone project individual, namun saran dan feedback sangat diterima:

1. Open issue untuk bug reports
2. Submit pull request untuk improvements
3. Share ideas di discussions

---

## 📧 Contact

**Ivan David**  
- Student ID: B25B8M113
- Program: Dicoding Bootcamp - Machine Learning
- Email: [your-email]
- GitHub: [your-github]

---

## 📄 License

This project is created for educational purposes as part of Dicoding Bootcamp Capstone Project.

---

## ⭐ Acknowledgments

- **Dicoding Indonesia** - Platform & mentoring
- **SKU-110K Authors** - Amazing dataset
- **Ultralytics** - YOLOv8 framework
- **TensorFlow Team** - ML framework

---

## 🎉 Let's Build Something Amazing!

**Current Status:** 🟢 Dataset Setup & Exploration Phase

**Next Milestone:** Object Detection Model Training

**Progress:** ████░░░░░░ 20%

---

**Last Updated:** Oktober 2025
