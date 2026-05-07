## Quick Start Guide

### 1. Setup Environment (One-time)

```bash
# Windows (cmd)
python -m venv venv
venv\Scripts\activate.bat

# Windows (PowerShell)
python -m venv venv
venv\Scripts\Activate.ps1

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Capture Training Images

```bash
python scripts/capture.py
```
- Press **SPACE** to save, **Q** to quit
- Aim for 30-100 images of salamanders
- Variety: different angles, distances, lighting, backgrounds

### 4. Prepare Dataset

```bash
python scripts/prepare_dataset.py \
  --input data/captured \
  --output data/dataset \
  --train-ratio 0.7 \
  --val-ratio 0.2
```

Label images manually by editing `.txt` files in `data/dataset/labels/` with format:
```
class_id x_center y_center width height
0 0.5 0.5 0.3 0.4
```

Or use Label Studio (see README.md)

### 5. Train Model

```bash
python scripts/train.py \
  --model yolo11n.pt \
  --data data/dataset/dataset.yaml \
  --epochs 50 \
  --imgsz 320 \
  --batch 8 \
  --name salamander_v1
```

Model saved to: `runs/detect/salamander_v1/weights/best.pt`

### 6. Process Video

```bash
python scripts/video_inference.py \
  --weights runs/detect/salamander_v1/weights/best.pt \
  --input data/videos/sample.mp4 \
  --output results/sample_annotated.mp4 \
  --csv results/detections.csv
```

**Outputs:**
- `results/sample_annotated.mp4` - Video with bounding boxes
- `results/detections.csv` - Frame-by-frame detections

### 7. Live Webcam (Optional)

```bash
python scripts/live_inference.py \
  --weights runs/detect/salamander_v1/weights/best.pt \
  --conf 0.5
```

---

## Directory Structure Created

```
backend/
├── scripts/              # All Python scripts
├── data/
│   ├── captured/        # Raw webcam images (output of capture.py)
│   ├── dataset/         # Labeled YOLO dataset
│   │   ├── images/
│   │   │   ├── train/   # Training images
│   │   │   ├── val/     # Validation images
│   │   │   └── test/    # Test images
│   │   ├── labels/      # Bounding box annotations
│   │   └── dataset.yaml # Dataset config
│   └── videos/          # Video files to process
├── results/             # Output videos & CSVs
└── runs/                # Training outputs (created by train.py)
```

---

## Tips

**Speed up training:**
```bash
python scripts/train.py --epochs 25 --imgsz 320 --batch 16
```

**Better accuracy (slower):**
```bash
python scripts/train.py --model yolo11m.pt --epochs 100 --imgsz 640
```

**CPU only:**
```bash
python scripts/train.py --device cpu
```

**Process every 2nd frame (faster):**
```bash
python scripts/video_inference.py --skip-frames 2 ...
```

---

See [README.md](README.md) for detailed documentation.
