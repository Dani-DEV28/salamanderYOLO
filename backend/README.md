# YOLO Video Processing Backend

A simple, script-based YOLO system for training custom object detectors and processing videos. Adapted from the Applied-AI-YOLO-Walkthrough but optimized for salamander detection in videos.

## What you can do

1. **Capture training images** from your webcam
2. **Label images** in Label Studio
3. **Prepare dataset** in YOLO format
4. **Visualize augmentations** as a PDF
5. **Train custom YOLO models** fine-tuned on your data
6. **Process videos** with bounding boxes, tracking, and CSV export
7. **Run live inference** on webcam with counting and timing

## Prerequisites

- Python 3.9 or newer
- Webcam (for capture.py)
- ~2 GB free disk space

## One-time Setup

### 1. Create Virtual Environment

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows (PowerShell):**
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

**Windows (cmd.exe):**
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Verify Installation

```bash
python -c "from ultralytics import YOLO; import cv2; print('ok')"
```

---

## Project Structure

```
backend/
├── scripts/
│   ├── capture.py              # Capture training images from webcam
│   ├── prepare_dataset.py       # Convert captured images to YOLO format
│   ├── visualize_augmentations.py
│   ├── train.py                # Train custom YOLO model
│   ├── live_inference.py       # Live webcam inference with tracking
│   ├── video_inference.py      # Process videos (NEW!)
│   └── utils.py                # Shared utilities
├── data/
│   ├── captured/               # Raw webcam captures (from capture.py)
│   ├── dataset/                # Labeled dataset (YOLO format)
│   │   ├── images/
│   │   │   ├── train/
│   │   │   ├── val/
│   │   │   └── test/
│   │   ├── labels/
│   │   │   ├── train/
│   │   │   ├── val/
│   │   │   └── test/
│   │   └── dataset.yaml
│   └── videos/                 # Videos to process
├── runs/                       # Training outputs
│   └── detect/
│       └── run1/
│           └── weights/
│               └── best.pt
├── results/                    # Video processing outputs (CSV, annotated videos)
├── yolo11n.pt                 # Pre-trained base model
├── requirements.txt
└── README.md
```

---

## Workflow: Complete Training Pipeline

### Step 1: Capture Training Images

```bash
python scripts/capture.py
```

- Opens your webcam
- Press **SPACE** to save frame, **Q** to quit
- Aim for 30-100 images
- Variety matters: different angles, distances, lighting, backgrounds

Frames land in `data/captured/`

### Step 2: Label Images in Label Studio

```bash
docker-compose up -d
# Open http://localhost:8080
```

Or skip and manually create bounding boxes in the `.txt` files.

### Step 3: Prepare Dataset

```bash
python scripts/prepare_dataset.py \
  --input data/captured \
  --output data/dataset \
  --train-ratio 0.7 \
  --val-ratio 0.2
```

Creates:
- YOLO-format folder structure
- `data/dataset/dataset.yaml` configuration
- Train/val/test splits

### Step 4: Visualize Augmentations (Optional)

```bash
python scripts/visualize_augmentations.py \
  --data data/dataset/dataset.yaml \
  --output augmentations.pdf
```

Shows what each augmentation does to your images.

### Step 5: Train Custom Model

```bash
python scripts/train.py \
  --model yolo11n.pt \
  --data data/dataset/dataset.yaml \
  --epochs 50 \
  --imgsz 320 \
  --batch 8 \
  --name my_salamander_model
```

**Outputs:**
- Trained weights: `runs/detect/my_salamander_model/weights/best.pt`
- Training metrics: `runs/detect/my_salamander_model/results.csv`
- Confusion matrix, precision/recall graphs, etc.

### Step 6: Run Live Inference (Webcam)

```bash
python scripts/live_inference.py \
  --weights runs/detect/my_salamander_model/weights/best.pt \
  --conf 0.5 \
  --imgsz 320
```

Displays:
- Live bounding boxes
- Count of objects per class
- Cumulative seconds each class has been on screen

Press **Q** to quit.

### Step 7: Process Videos 🎥

```bash
python scripts/video_inference.py \
  --weights runs/detect/my_salamander_model/weights/best.pt \
  --input data/videos/sample.mp4 \
  --output results/sample_annotated.mp4 \
  --csv results/sample_detections.csv \
  --conf 0.5 \
  --imgsz 320
```

**Outputs:**
- Annotated video with bounding boxes: `sample_annotated.mp4`
- Detections as CSV: `sample_detections.csv`

CSV contains:
```
frame,timestamp,class_id,class_name,confidence,x_min,y_min,x_max,y_max,x_center,y_center
0,0.0,0,salamander,0.95,100,150,250,400,175,275
1,0.033,0,salamander,0.92,105,155,245,395,175,275
...
```

---

## All Scripts Reference

### capture.py
```bash
python scripts/capture.py [--camera CAMERA]
```

Capture images from webcam for training dataset.

**Keys:**
- SPACE: Save current frame
- Q/ESC: Quit

### prepare_dataset.py
```bash
python scripts/prepare_dataset.py \
  --input DIR \
  --output DIR \
  [--train-ratio 0.7] \
  [--val-ratio 0.2]
```

Convert raw images to YOLO format with train/val/test splits.

### visualize_augmentations.py
```bash
python scripts/visualize_augmentations.py \
  --data YAML \
  [--output augmentations.pdf]
```

Generate PDF showing all augmentations on sample images.

### train.py
```bash
python scripts/train.py \
  [--model MODEL] \
  [--data YAML] \
  [--epochs EPOCHS] \
  [--imgsz SIZE] \
  [--batch BATCH] \
  [--name NAME] \
  [--device DEVICE]
```

Fine-tune YOLO model on dataset.

**Augmentation tuning:**
```bash
python scripts/train.py \
  --hsv-h 0.015 \
  --hsv-s 0.7 \
  --hsv-v 0.4 \
  --fliplr 0.5 \
  --scale 0.5
```

### live_inference.py
```bash
python scripts/live_inference.py \
  [--weights PATH] \
  [--conf CONF] \
  [--imgsz SIZE] \
  [--camera CAMERA]
```

Run live detection on webcam with counting and timing.

### video_inference.py (NEW)
```bash
python scripts/video_inference.py \
  --weights PATH \
  --input VIDEO \
  [--output VIDEO] \
  [--csv CSV] \
  [--conf CONF] \
  [--imgsz SIZE] \
  [--skip-frames N]
```

Process video file with YOLO detection. Outputs annotated video and CSV.

---

## Data Structure Details

### YOLO Dataset Format

Each image must have a corresponding `.txt` label file:

```
images/
  train/
    photo1.jpg    -->  labels/train/photo1.txt
    photo2.jpg    -->  labels/train/photo2.txt
labels/
  train/
    photo1.txt     (contains: class_id x_center y_center width height)
    photo2.txt
```

Label file format (normalized coordinates):
```
0 0.5 0.5 0.3 0.4
```
= Class 0, center at 50%, 50%, width 30%, height 40%

### dataset.yaml

```yaml
path: /absolute/path/to/data/dataset
train: images/train
val: images/val
test: images/test
nc: 1
names: ['salamander']
```

---

## Tips & Tricks

### Faster Training
- Use `--imgsz 320` instead of 640
- Use `yolo11n.pt` instead of larger models
- Reduce `--epochs` to 25-30

### Better Accuracy
- Capture more diverse images (50-200)
- Use larger model: `yolo11m.pt`
- Increase `--imgsz 640`
- Add augmentation variations

### Debug Training
- Check `runs/detect/<name>/results.csv` for metrics
- View confusion matrix: `runs/detect/<name>/confusion_matrix.png`
- Tensorboard: `tensorboard --logdir runs/detect`

### Video Processing Speed
- Use `--skip-frames 2` to process every 2nd frame
- Use smaller `--imgsz` (320 instead of 640)
- Use smaller model (yolo11n instead of yolo11l)

---

## Troubleshooting

### ModuleNotFoundError: No module named 'ultralytics'
Forgot to activate venv:
```bash
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate.bat # Windows
```

### No module named 'cv2'
```bash
pip install opencv-python
```

### CUDA out of memory
- Reduce `--batch` size
- Use `--device cpu` to use CPU instead
- Use smaller model (`yolo11n`)

### Webcam access denied (macOS)
Grant camera permission:
1. System Settings > Privacy & Security > Camera
2. Add your terminal to allowed apps

---

## Files & Outputs

| File | Created By | Purpose |
|------|-----------|---------|
| `data/captured/` | capture.py | Raw webcam frames |
| `data/dataset/` | prepare_dataset.py | Labeled YOLO dataset |
| `runs/detect/run1/` | train.py | Trained model + metrics |
| `results/` | video_inference.py | Annotated videos + CSVs |

---

## References

- [Ultralytics YOLOv8/v11 Docs](https://docs.ultralytics.com/)
- [YOLO Dataset Format](https://docs.ultralytics.com/datasets/detect/)
- [YOLO Augmentation Reference](https://docs.ultralytics.com/usage/operations/predict/)
