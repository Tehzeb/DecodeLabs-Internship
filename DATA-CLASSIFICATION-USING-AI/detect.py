"""
detect.py  —  Run detection on images, video, or webcam
Commands:
  python detect.py --source dataset/images/test        # whole folder
  python detect.py --source myimage.jpg                # one image
  python detect.py --source myvideo.mp4                # video file
  python detect.py --source 0                          # live webcam
"""
import argparse, os, cv2
from ultralytics import YOLO

WEIGHTS = "runs/detect/runs/helmet_v1/weights/best.pt"
CONF     = 0.5
OUT_DIR  = "output"
COLORS   = {0: (30,180,80), 1: (210,40,40)}   # green=helmet  red=no_helmet
LABELS   = {0: "Helmet", 1: "No Helmet"}

def load_model():
    if not os.path.exists(WEIGHTS):
        raise FileNotFoundError(
            f"\n  [ERROR] {WEIGHTS} not found.\n"
            "  Run  python train.py  first to create the weights.\n")
    return YOLO(WEIGHTS)

def annotate(img, results):
    out = img.copy()
    h_count = nh_count = 0
    for box in results.boxes:
        cls  = int(box.cls[0])
        conf = float(box.conf[0])
        x1,y1,x2,y2 = map(int, box.xyxy[0])
        color = COLORS.get(cls,(200,200,200))
        text  = f"{LABELS.get(cls,'?')}  {conf:.0%}"
        cv2.rectangle(out,(x1,y1),(x2,y2),color,2)
        (tw,th),_= cv2.getTextSize(text,cv2.FONT_HERSHEY_SIMPLEX,0.55,1)
        cv2.rectangle(out,(x1,y1-th-8),(x1+tw+6,y1),color,-1)
        cv2.putText(out,text,(x1+3,y1-4),cv2.FONT_HERSHEY_SIMPLEX,0.55,(255,255,255),1)
        if cls==0: h_count+=1
        else:      nh_count+=1
    summary = f"  Helmet:{h_count}   No Helmet:{nh_count}  "
    (sw,sh),_=cv2.getTextSize(summary,cv2.FONT_HERSHEY_SIMPLEX,0.6,1)
    cv2.rectangle(out,(0,0),(sw+6,sh+10),(20,20,20),-1)
    cv2.putText(out,summary,(4,sh+2),cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,255,255),1)
    return out, h_count, nh_count

def run_image(model, path):
    img = cv2.imread(path)
    if img is None: return print(f"  Cannot read: {path}")
    res = model.predict(path, conf=CONF, verbose=False)[0]
    out,h,nh = annotate(img, res)
    os.makedirs(OUT_DIR, exist_ok=True)
    dst = os.path.join(OUT_DIR, "det_" + os.path.basename(path))
    cv2.imwrite(dst, out)
    status = "✓ SAFE" if nh==0 else "✗ VIOLATION"
    print(f"  {os.path.basename(path):<30}  Helmet:{h}  No-Helmet:{nh}  {status}")
    print(f"  Saved → {dst}")

def run_folder(model, folder):
    imgs = [f for f in os.listdir(folder)
            if f.lower().endswith((".jpg",".jpeg",".png",".bmp"))]
    if not imgs: return print(f"  No images in {folder}")
    print(f"\n  Running on {len(imgs)} images...\n")
    for f in sorted(imgs):
        run_image(model, os.path.join(folder, f))

def run_video(model, src):
    cap = cv2.VideoCapture(int(src) if src=="0" else src)
    if not cap.isOpened(): return print(f"  Cannot open: {src}")
    fps = cap.get(cv2.CAP_PROP_FPS) or 25
    w   = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h   = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    os.makedirs(OUT_DIR, exist_ok=True)
    name  = "webcam.mp4" if src=="0" else os.path.basename(src)
    dst   = os.path.join(OUT_DIR,"det_"+name)
    writer= cv2.VideoWriter(dst,cv2.VideoWriter_fourcc(*"mp4v"),fps,(w,h))
    n=0
    print("  Press Q to quit (webcam mode)...")
    while True:
        ret, frame = cap.read()
        if not ret: break
        res = model.predict(frame, conf=CONF, verbose=False)[0]
        out,_,_ = annotate(frame, res)
        writer.write(out)
        cv2.imshow("Helmet Detection — Q to quit", out)
        n+=1
        if cv2.waitKey(1) & 0xFF == ord("q"): break
    cap.release(); writer.release(); cv2.destroyAllWindows()
    print(f"  {n} frames processed.  Saved → {dst}")

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default="dataset/images/test")
    args = parser.parse_args()
    model = load_model()
    src = args.source
    if src=="0" or src.lower().endswith((".mp4",".avi",".mov")):
        run_video(model, src)
    elif os.path.isdir(src):
        run_folder(model, src)
    else:
        run_image(model, src)
