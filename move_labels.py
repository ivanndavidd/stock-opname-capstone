#!/usr/bin/env python3
"""
Move labels from data/YOLO/labels/ to data/labels/
untuk memenuhi struktur yang dibutuhkan YOLOv8
"""

import os
import shutil
from pathlib import Path

def move_labels():
    """Move labels dari YOLO subfolder ke data folder"""
    
    print("="*70)
    print("🔄 MOVING LABELS TO CORRECT LOCATION")
    print("="*70)
    
    # Paths
    src_base = Path("data/YOLO/labels")
    dst_base = Path("data/labels")
    
    # Check if source exists
    if not src_base.exists():
        print(f"❌ Source tidak ditemukan: {src_base}")
        print("   Labels mungkin sudah di lokasi yang benar")
        
        # Check if already in correct location
        if dst_base.exists():
            print(f"\n✅ Labels sudah ada di: {dst_base}")
            for split in ['train', 'val', 'test']:
                split_dir = dst_base / split
                if split_dir.exists():
                    txt_files = list(split_dir.glob("*.txt"))
                    print(f"   • {split}: {len(txt_files)} files")
        return
    
    print(f"\n📂 Source: {src_base}")
    print(f"📂 Destination: {dst_base}")
    
    # Create destination directory
    dst_base.mkdir(parents=True, exist_ok=True)
    
    # Move each split
    total_moved = 0
    for split in ['train', 'val', 'test']:
        src_split = src_base / split
        dst_split = dst_base / split
        
        if not src_split.exists():
            print(f"\n⚠️  {split}: Source tidak ditemukan")
            continue
        
        print(f"\n📦 Moving {split}...")
        
        # Count source files
        src_files = list(src_split.glob("*.txt"))
        print(f"   Source: {len(src_files)} files")
        
        # Remove destination if exists
        if dst_split.exists():
            print(f"   Removing old destination...")
            shutil.rmtree(dst_split)
        
        # Move directory
        shutil.move(str(src_split), str(dst_split))
        
        # Verify
        dst_files = list(dst_split.glob("*.txt"))
        print(f"   ✓ Moved: {len(dst_files)} files")
        total_moved += len(dst_files)
    
    # Cleanup empty YOLO directory
    try:
        if src_base.exists() and not any(src_base.iterdir()):
            src_base.rmdir()
            print(f"\n🗑️  Removed empty directory: {src_base}")
        
        yolo_dir = Path("data/YOLO")
        if yolo_dir.exists() and not any(yolo_dir.iterdir()):
            yolo_dir.rmdir()
            print(f"🗑️  Removed empty directory: {yolo_dir}")
    except Exception as e:
        print(f"⚠️  Cleanup warning: {e}")
    
    print("\n" + "="*70)
    print(f"✅ LABELS MOVED SUCCESSFULLY!")
    print(f"   Total files moved: {total_moved}")
    print("="*70)
    
    print("\n📁 New structure:")
    print("""
data/
├── images/
│   ├── train/
│   ├── val/
│   └── test/
├── annotations/
└── labels/           ← Labels sekarang di sini!
    ├── train/
    ├── val/
    └── test/
    """)
    
    print("🎯 Next step: Update data.yaml dan start training!")

def verify_structure():
    """Verify labels are in correct location"""
    print("\n" + "="*70)
    print("🔍 VERIFYING STRUCTURE")
    print("="*70)
    
    images_dir = Path("data/images")
    labels_dir = Path("data/labels")
    
    if not labels_dir.exists():
        print("❌ Labels directory tidak ditemukan!")
        return False
    
    all_good = True
    for split in ['train', 'val', 'test']:
        img_split = images_dir / split
        lbl_split = labels_dir / split
        
        if not img_split.exists():
            print(f"⚠️  {split}: Images directory tidak ditemukan")
            all_good = False
            continue
        
        if not lbl_split.exists():
            print(f"⚠️  {split}: Labels directory tidak ditemukan")
            all_good = False
            continue
        
        # Count files
        img_files = list(img_split.glob("*.jpg"))
        lbl_files = list(lbl_split.glob("*.txt"))
        
        print(f"\n{split}:")
        print(f"  Images: {len(img_files)} files")
        print(f"  Labels: {len(lbl_files)} files")
        
        if len(img_files) == len(lbl_files):
            print(f"  ✓ Match!")
        else:
            print(f"  ⚠️  Mismatch!")
            all_good = False
    
    print("\n" + "="*70)
    if all_good:
        print("✅ STRUCTURE VERIFIED - Ready for training!")
    else:
        print("⚠️  ISSUES FOUND - Please check above")
    print("="*70)
    
    return all_good

if __name__ == "__main__":
    import sys
    
    # Parse arguments
    verify_only = '--verify' in sys.argv
    
    if verify_only:
        verify_structure()
    else:
        move_labels()
        verify_structure()
