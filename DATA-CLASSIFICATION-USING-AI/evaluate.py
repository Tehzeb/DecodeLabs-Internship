"""
evaluate.py  —  Generate all metrics and report figures
Command : python evaluate.py
"""
import os, shutil
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from ultralytics import YOLO

WEIGHTS = "runs/detect/runs/helmet_v1/weights/best.pt"
DATA     = "dataset.yaml"
OUT_DIR  = "report_figures"

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    if not os.path.exists(WEIGHTS):
        raise FileNotFoundError(f"Run train.py first — {WEIGHTS} not found")

    model = YOLO(WEIGHTS)
    print("\n  Evaluating on test set...\n")
    m = model.val(data=DATA, imgsz=640, split="test",
                  plots=True, project=OUT_DIR, name="eval", verbose=False)

    map50  = m.box.map50
    map    = m.box.map
    prec   = m.box.mp
    recall = m.box.mr

    print(f"\n{'='*48}")
    print(f"  {'mAP@0.5 (main metric)':<30} {map50*100:>6.1f}%")
    print(f"  {'mAP@0.5:0.95':<30} {map*100:>6.1f}%")
    print(f"  {'Precision':<30} {prec*100:>6.1f}%")
    print(f"  {'Recall':<30} {recall*100:>6.1f}%")
    print(f"{'='*48}")

    # Copy training plots
    for f in ["results.png","confusion_matrix.png","PR_curve.png","F1_curve.png"]:
        src = os.path.join("runs","helmet_v1",f)
        if os.path.exists(src):
            shutil.copy(src, os.path.join(OUT_DIR, f))

    # Clean summary bar chart
    fig, ax = plt.subplots(figsize=(7,4))
    names = ["mAP@0.5","mAP@0.5:0.95","Precision","Recall"]
    vals  = [map50*100, map*100, prec*100, recall*100]
    colors= ["#534AB7","#1D9E75","#D85A30","#E0A020"]
    bars  = ax.bar(names, vals, color=colors, width=0.5, edgecolor="none")
    ax.set_ylim(0,110)
    ax.set_ylabel("Score (%)", fontsize=11)
    ax.set_title("YOLOv8 Helmet Detection — Evaluation Metrics", fontsize=13, pad=10)
    ax.spines[["top","right"]].set_visible(False)
    for b,v in zip(bars,vals):
        ax.text(b.get_x()+b.get_width()/2, b.get_height()+1.5,
                f"{v:.1f}%", ha="center", va="bottom", fontsize=11)
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR,"eval_summary.png"), dpi=150, bbox_inches="tight")
    plt.close()

    print(f"\n  All figures saved to  {OUT_DIR}/")
    print(f"  Use these in Chapter 5 of your report.")

if __name__=="__main__":
    main()
