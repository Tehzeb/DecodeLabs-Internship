"""
src/split_dataset.py
If all your images are in ONE folder, this splits them into train/val/test.
Command: python src/split_dataset.py --images path/to/images --labels path/to/labels
"""
import os, shutil, random, argparse
from pathlib import Path

def split(images_dir, labels_dir, train=0.7, val=0.2, test=0.1):
    exts  = {".jpg",".jpeg",".png",".bmp"}
    imgs  = [f for f in Path(images_dir).iterdir() if f.suffix.lower() in exts]
    if not imgs: return print(f"No images found in {images_dir}")
    random.seed(42); random.shuffle(imgs)
    n  = len(imgs)
    nt = int(n*train); nv = int(n*val)
    splits = {"train":imgs[:nt], "val":imgs[nt:nt+nv], "test":imgs[nt+nv:]}
    print(f"\n  Total:{n}  Train:{nt}  Val:{nv}  Test:{n-nt-nv}\n")
    for split_name, flist in splits.items():
        id_ = Path(f"dataset/images/{split_name}")
        ld_ = Path(f"dataset/labels/{split_name}")
        id_.mkdir(parents=True, exist_ok=True)
        ld_.mkdir(parents=True, exist_ok=True)
        for img in flist:
            shutil.copy(img, id_/img.name)
            lbl = Path(labels_dir)/(img.stem+".txt")
            if lbl.exists(): shutil.copy(lbl, ld_/lbl.name)
            else: print(f"  [WARN] no label for {img.name}")
        print(f"  {split_name}: {len(flist)} images copied")
    print("\n  Split complete!")

if __name__=="__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--images", required=True)
    p.add_argument("--labels", required=True)
    args = p.parse_args()
    split(args.images, args.labels)
