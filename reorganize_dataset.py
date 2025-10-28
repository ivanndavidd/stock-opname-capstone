"""
Script untuk Reorganize SKU-110K Dataset
Memindahkan images dari 1 folder ke struktur train/val/test

Author: Ivan David
Usage: python reorganize_dataset.py
"""

import os
import shutil
import pandas as pd
from tqdm import tqdm

class DatasetReorganizer:
    def __init__(self, base_dir="./data"):  # Changed: No SKU110K subfolder
        self.base_dir = base_dir
        self.images_dir = os.path.join(base_dir, "images")
        self.annotations_dir = os.path.join(base_dir, "annotations")
        
        # Target directories
        self.train_dir = os.path.join(self.images_dir, "train")
        self.val_dir = os.path.join(self.images_dir, "val")
        self.test_dir = os.path.join(self.images_dir, "test")
    
    def create_directories(self):
        """Buat folder train/val/test"""
        print("📁 Membuat folder train/val/test...")
        os.makedirs(self.train_dir, exist_ok=True)
        os.makedirs(self.val_dir, exist_ok=True)
        os.makedirs(self.test_dir, exist_ok=True)
        print("✓ Folder berhasil dibuat")
    
    def get_image_list_from_annotations(self, split):
        """Dapatkan list images dari file annotations"""
        ann_file = os.path.join(self.annotations_dir, f"annotations_{split}.csv")
        
        if not os.path.exists(ann_file):
            print(f"⚠️  File tidak ditemukan: {ann_file}")
            return []
        
        # Read CSV without header, then assign column names
        df = pd.read_csv(ann_file, header=None)
        df.columns = ['image_name', 'x1', 'y1', 'x2', 'y2', 'class', 'image_width', 'image_height']
        
        image_list = df['image_name'].unique().tolist()
        return image_list
    
    def move_files(self, image_list, target_dir, split_name):
        """Pindahkan files ke target directory"""
        print(f"\n📦 Memindahkan {split_name} images...")
        
        moved_count = 0
        not_found_count = 0
        
        for image_name in tqdm(image_list, desc=f"Moving {split_name}"):
            src_path = os.path.join(self.images_dir, image_name)
            dst_path = os.path.join(target_dir, image_name)
            
            if os.path.exists(src_path):
                shutil.move(src_path, dst_path)
                moved_count += 1
            else:
                not_found_count += 1
        
        print(f"✓ Berhasil memindahkan: {moved_count} files")
        if not_found_count > 0:
            print(f"⚠️  Tidak ditemukan: {not_found_count} files")
        
        return moved_count, not_found_count
    
    def reorganize(self):
        """Main reorganize function"""
        print("\n" + "="*70)
        print("🔄 REORGANIZE SKU-110K DATASET")
        print("="*70)
        
        # Check if already organized
        if os.path.exists(self.train_dir) and len(os.listdir(self.train_dir)) > 0:
            print("\n⚠️  Dataset sudah ter-reorganize!")
            response = input("Apakah ingin reorganize ulang? (y/n): ")
            if response.lower() != 'y':
                print("Operasi dibatalkan.")
                return
            
            # Clear existing folders
            print("\n🗑️  Menghapus folder lama...")
            shutil.rmtree(self.train_dir, ignore_errors=True)
            shutil.rmtree(self.val_dir, ignore_errors=True)
            shutil.rmtree(self.test_dir, ignore_errors=True)
        
        # Create directories
        self.create_directories()
        
        # Get image lists from annotations
        print("\n📋 Membaca annotations...")
        train_images = self.get_image_list_from_annotations('train')
        val_images = self.get_image_list_from_annotations('val')
        test_images = self.get_image_list_from_annotations('test')
        
        print(f"  • Train: {len(train_images)} images")
        print(f"  • Val: {len(val_images)} images")
        print(f"  • Test: {len(test_images)} images")
        
        # Move files
        train_moved, train_not_found = self.move_files(train_images, self.train_dir, "train")
        val_moved, val_not_found = self.move_files(val_images, self.val_dir, "val")
        test_moved, test_not_found = self.move_files(test_images, self.test_dir, "test")
        
        # Summary
        print("\n" + "="*70)
        print("✅ REORGANIZE COMPLETE!")
        print("="*70)
        print(f"\n📊 Summary:")
        print(f"  • Train: {train_moved} files moved")
        print(f"  • Val: {val_moved} files moved")
        print(f"  • Test: {test_moved} files moved")
        print(f"  • Total: {train_moved + val_moved + test_moved} files")
        
        if train_not_found + val_not_found + test_not_found > 0:
            print(f"\n⚠️  Total files not found: {train_not_found + val_not_found + test_not_found}")
        
        print("\n📁 Struktur baru:")
        print(f"""
{self.base_dir}/
├── images/
│   ├── train/     ({train_moved} images)
│   ├── val/       ({val_moved} images)
│   └── test/      ({test_moved} images)
└── annotations/
    ├── annotations_train.csv
    ├── annotations_val.csv
    └── annotations_test.csv
        """)
        
        # Check for remaining files
        remaining_files = [f for f in os.listdir(self.images_dir) 
                          if f.endswith('.jpg') or f.endswith('.png')]
        
        if remaining_files:
            print(f"\n⚠️  Ada {len(remaining_files)} files tersisa di folder images/")
            print("Files ini mungkin tidak ada di annotations atau duplikat.")
        
        print("\n✨ Dataset siap untuk training!")
        print("="*70)

class DatasetValidator:
    """Validasi dataset setelah reorganize"""
    
    def __init__(self, base_dir="./data"):  # Changed: No SKU110K subfolder
        self.base_dir = base_dir
        self.images_dir = os.path.join(base_dir, "images")
        self.annotations_dir = os.path.join(base_dir, "annotations")
    
    def validate(self):
        """Validasi struktur dan integritas dataset"""
        print("\n" + "="*70)
        print("🔍 VALIDASI DATASET")
        print("="*70)
        
        splits = ['train', 'val', 'test']
        all_valid = True
        
        for split in splits:
            print(f"\n📊 Checking {split}...")
            
            # Check folder
            img_dir = os.path.join(self.images_dir, split)
            if not os.path.exists(img_dir):
                print(f"  ✗ Folder tidak ditemukan: {img_dir}")
                all_valid = False
                continue
            
            # Count images
            images = [f for f in os.listdir(img_dir) if f.endswith(('.jpg', '.png'))]
            print(f"  • Images di folder: {len(images)}")
            
            # Check annotations
            ann_file = os.path.join(self.annotations_dir, f"annotations_{split}.csv")
            if not os.path.exists(ann_file):
                print(f"  ✗ Annotations tidak ditemukan: {ann_file}")
                all_valid = False
                continue
            
            # Read CSV without header, then assign column names
            df = pd.read_csv(ann_file, header=None)
            df.columns = ['image_name', 'x1', 'y1', 'x2', 'y2', 'class', 'image_width', 'image_height']
            
            unique_images = df['image_name'].nunique()
            total_annotations = len(df)
            
            print(f"  • Images di annotations: {unique_images}")
            print(f"  • Total annotations: {total_annotations}")
            print(f"  • Avg objects/image: {total_annotations/unique_images:.2f}")
            
            # Check consistency
            if len(images) == unique_images:
                print(f"  ✓ Images match dengan annotations")
            else:
                print(f"  ⚠️  Mismatch: {len(images)} files vs {unique_images} dalam annotations")
                all_valid = False
        
        print("\n" + "="*70)
        if all_valid:
            print("✅ VALIDASI BERHASIL - Dataset siap digunakan!")
        else:
            print("⚠️  ADA MASALAH - Periksa error di atas")
        print("="*70)

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Reorganize SKU-110K Dataset')
    parser.add_argument('--base-dir', type=str, default='./data',
                       help='Base directory dataset')
    parser.add_argument('--validate-only', action='store_true',
                       help='Hanya validasi tanpa reorganize')
    
    args = parser.parse_args()
    
    if args.validate_only:
        validator = DatasetValidator(base_dir=args.base_dir)
        validator.validate()
    else:
        # Reorganize
        reorganizer = DatasetReorganizer(base_dir=args.base_dir)
        reorganizer.reorganize()
        
        # Validate after reorganize
        validator = DatasetValidator(base_dir=args.base_dir)
        validator.validate()

if __name__ == "__main__":
    main()