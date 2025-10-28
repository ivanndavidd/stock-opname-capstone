"""
Script untuk Download dan Setup SKU-110K Dataset
Dataset: https://github.com/eg4000/SKU110K_CVPR19

Author: Ivan David
Project: Stock Opname Monitoring
"""

import os
import requests
import zipfile
from tqdm import tqdm
import shutil

class SKU110KDownloader:
    def __init__(self, base_dir="./data"):
        self.base_dir = base_dir
        self.dataset_dir = os.path.join(base_dir, "SKU110K")
        
        # URLs untuk download
        self.urls = {
            "images": "https://www.kaggle.com/datasets/thedagger/sku110k-annotations/download",
            "annotations": "https://www.kaggle.com/datasets/thedagger/sku110k-annotations/download"
        }
        
        # Struktur folder
        self.folders = {
            "images": os.path.join(self.dataset_dir, "images"),
            "train": os.path.join(self.dataset_dir, "images", "train"),
            "val": os.path.join(self.dataset_dir, "images", "val"),
            "test": os.path.join(self.dataset_dir, "images", "test"),
            "annotations": os.path.join(self.dataset_dir, "annotations")
        }
    
    def create_folders(self):
        """Buat struktur folder untuk dataset"""
        print("📁 Membuat struktur folder...")
        for folder_name, folder_path in self.folders.items():
            os.makedirs(folder_path, exist_ok=True)
            print(f"  ✓ {folder_name}: {folder_path}")
    
    def download_file(self, url, destination):
        """Download file dengan progress bar"""
        print(f"\n⬇️  Downloading: {os.path.basename(destination)}")
        
        response = requests.get(url, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        
        with open(destination, 'wb') as file, tqdm(
            desc=destination,
            total=total_size,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
        ) as progress_bar:
            for data in response.iter_content(chunk_size=1024):
                size = file.write(data)
                progress_bar.update(size)
    
    def manual_download_instructions(self):
        """Instruksi manual download karena SKU-110K butuh akses Google Drive"""
        print("\n" + "="*70)
        print("🔗 INSTRUKSI MANUAL DOWNLOAD SKU-110K DATASET")
        print("="*70)
        print("""
Dataset SKU-110K perlu didownload secara manual dari:

1. 📦 IMAGES:
   - Link: https://drive.google.com/file/d/1iq93lCdhaPUN0fhbJmBu6FP2-FpGp0kp/view
   - File: SKU110K_fixed.tar.gz (Ukuran: ~13GB)
   
2. 📋 ANNOTATIONS:
   - Link: https://github.com/eg4000/SKU110K_CVPR19
   - Clone repository atau download annotations folder

ATAU gunakan alternatif dari Kaggle (lebih mudah):
   - https://www.kaggle.com/datasets/thedagger/sku110k-annotations

LANGKAH-LANGKAH:
1. Download SKU110K_fixed.tar.gz dari Google Drive
2. Extract ke folder: {}/
3. Jalankan script ini lagi dengan: python setup_dataset.py --skip-download

STRUKTUR FOLDER YANG DIHARAPKAN:
{}
├── images/
│   ├── train/
│   ├── val/
│   └── test/
└── annotations/
    ├── annotations_train.csv
    ├── annotations_val.csv
    └── annotations_test.csv
        """.format(self.dataset_dir, self.dataset_dir))
        print("="*70)
    
    def verify_dataset(self):
        """Verifikasi apakah dataset sudah lengkap"""
        print("\n🔍 Verifikasi dataset...")
        
        required_files = {
            "Train Images": os.path.join(self.folders["train"]),
            "Val Images": os.path.join(self.folders["val"]),
            "Test Images": os.path.join(self.folders["test"]),
            "Train Annotations": os.path.join(self.folders["annotations"], "annotations_train.csv"),
            "Val Annotations": os.path.join(self.folders["annotations"], "annotations_val.csv"),
            "Test Annotations": os.path.join(self.folders["annotations"], "annotations_test.csv")
        }
        
        all_exists = True
        for name, path in required_files.items():
            exists = os.path.exists(path)
            status = "✓" if exists else "✗"
            print(f"  {status} {name}: {path}")
            if not exists:
                all_exists = False
        
        if all_exists:
            print("\n✅ Dataset lengkap dan siap digunakan!")
            self.print_dataset_stats()
        else:
            print("\n⚠️  Dataset belum lengkap. Ikuti instruksi manual download.")
        
        return all_exists
    
    def print_dataset_stats(self):
        """Tampilkan statistik dataset"""
        print("\n📊 Statistik Dataset:")
        
        for split in ["train", "val", "test"]:
            img_folder = self.folders[split]
            if os.path.exists(img_folder):
                num_images = len([f for f in os.listdir(img_folder) if f.endswith(('.jpg', '.png'))])
                print(f"  • {split.capitalize()}: {num_images} images")
    
    def setup(self, skip_download=False):
        """Main setup function"""
        print("\n" + "="*70)
        print("🎯 SKU-110K DATASET SETUP")
        print("="*70)
        
        # Buat folder
        self.create_folders()
        
        # Cek apakah dataset sudah ada
        if self.verify_dataset():
            print("\n✨ Setup selesai! Dataset siap digunakan.")
            return True
        
        # Jika belum ada, tampilkan instruksi
        if not skip_download:
            self.manual_download_instructions()
            return False
        
        return False

# Alternative: Quick start dengan subset kecil untuk testing
class SKU110KQuickStart:
    """Download subset kecil untuk testing cepat"""
    
    def __init__(self, base_dir="./data"):
        self.base_dir = base_dir
        self.sample_dir = os.path.join(base_dir, "SKU110K_sample")
    
    def create_sample_dataset(self, num_samples=100):
        """Buat sample dataset kecil dari full dataset"""
        print("\n🎨 Membuat sample dataset untuk testing...")
        print(f"Mengambil {num_samples} sample images...")
        
        # Implementasi untuk copy sample files
        # (akan dijalankan setelah full dataset terdownload)
        pass

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Setup SKU-110K Dataset')
    parser.add_argument('--skip-download', action='store_true', 
                       help='Skip download instructions (jika sudah manual download)')
    parser.add_argument('--base-dir', type=str, default='./data',
                       help='Base directory untuk dataset')
    
    args = parser.parse_args()
    
    # Setup dataset
    downloader = SKU110KDownloader(base_dir=args.base_dir)
    downloader.setup(skip_download=args.skip_download)
