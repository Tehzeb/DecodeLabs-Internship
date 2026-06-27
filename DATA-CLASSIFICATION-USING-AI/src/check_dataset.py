"""
src/check_dataset.py  —  Verify dataset structure and visualise samples
Command : python src/check_dataset.py
"""
import os, random, cv2
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

NAMES  = {0:"Helmet", 1:"No Helmet"}
COLORS = {0:(30,180,80), 1:(210,40,40)}

def draw_boxes(img_path, lbl_path):
    img = cv2.imread(img_path)
    if img is None: return None
    h,w = img.shape[:2]
    out = img.copy()
    if os.path.exists(lbl_path):
        with open(lbl_path) as f:
            for line in f:
                p = line.strip().split()
                if len(p)!=5: continue
                c = int(p[0])
                cx,cy,bw,bh = map(float,p[1:])
                x1=int((cx-bw/2)*w); y1=int((cy-bh/2)*h)
                x2=int((cx+bw/2)*w); y2=int((cy+bh/2)*h)
                col = COLORS.get(c,(200,200,200))
                lbl = NAMES.get(c,str(c))
                cv2.rectangle(out,(x1,y1),(x2,y2),col,2)
                cv2.rectangle(out,(x1,y1-18),(x1+len(lbl)*9,y1),col,-1)
                cv2.putText(out,lbl,(x1+2,y1-3),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),1)
    return out

def visualize(split="train", n=9):
    img_dir = Path(f"dataset/images/{split}")
    lbl_dir = Path(f"dataset/labels/{split}")
    imgs = list(img_dir.glob("*.jpg"))+list(img_dir.glob("*.png"))
    if not imgs:
        print(f"  [WARN] No images in dataset/images/{split}/")
        return
    sample = random.sample(imgs, min(n, len(imgs)))
    cols   = 3; rows = (len(sample)+cols-1)//cols
    fig,axes = plt.subplots(rows, cols, figsize=(14, 5*rows))
    fig.suptitle(f"Dataset samples — {split}  ({len(imgs)} images)", fontsize=13)
    for i,ax in enumerate(axes.flat):
        if i<len(sample):
            ann = draw_boxes(str(sample[i]), str(lbl_dir/(sample[i].stem+".txt")))
            ax.imshow(cv2.cvtColor(ann, cv2.COLOR_BGR2RGB))
            ax.set_title(sample[i].name, fontsize=8)
        ax.axis("off")
    plt.tight_layout()
    os.makedirs("report_figures", exist_ok=True)
    out = f"report_figures/samples_{split}.png"
    plt.savefig(out, dpi=120, bbox_inches="tight"); plt.close()
    print(f"  Saved: {out}")

def verify():
    ok = bad = 0
    for split in ["train","val","test"]:
        img_dir = Path(f"dataset/images/{split}")
        lbl_dir = Path(f"dataset/labels/{split}")
        imgs = list(img_dir.glob("*.jpg"))+list(img_dir.glob("*.png"))
        counts = {0:0, 1:0}
        for img in imgs:
            lbl = lbl_dir/(img.stem+".txt")
            if not lbl.exists(): bad+=1; continue
            with open(lbl) as f:
                for line in f:
                    p=line.strip().split()
                    if len(p)==5:
                        ok+=1; counts[int(p[0])]=counts.get(int(p[0]),0)+1
                    else: bad+=1
        print(f"\n  {split.upper():5s}  images:{len(imgs):4d}  "
              f"helmet:{counts[0]:4d}  no_helmet:{counts[1]:4d}")
    print(f"\n  Valid rows:{ok}   Issues:{bad}")
    if bad==0: print("  Dataset looks correct!")
    else:      print("  Fix issues before training.")

if __name__=="__main__":
    print("\n  Checking dataset...\n")
    verify()
    print("\n  Saving sample figures...")
    for s in ["train","val","test"]:
        visualize(s)
    print("\n  Open report_figures/ to check images have boxes drawn on them.")
