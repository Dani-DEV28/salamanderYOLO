import time
import cv2
import yaml
import ultralytics
import subprocess
from threading import Thread
from collections import defaultdict
from ultralytics import YOLO
from pathlib import Path
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from ultralytics.trackers import BYTETracker
from types import SimpleNamespace



VIDEOS_DIR = Path(__file__).parent / "videos"
VIDEOS_DIR.mkdir(exist_ok=True)

app = FastAPI(title="Salamander Tracker POC")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/videos", StaticFiles(directory=str(VIDEOS_DIR)), name="videos")
job = {"status": "idle"}

model = YOLO("best.pt")
print(model.names)

@app.get("/")
def root():
    return {"ok": True}

def run_track_job():
    # All the existing processing code from start_track moves here:
    # opening the video, setting up the writer, the frame loop with
    # YOLO inference and the per-track aggregation, the cap/writer
    # release calls, building the tracks list.
    input_path = VIDEOS_DIR / "input.mp4"

    cap = cv2.VideoCapture(str(input_path))
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"fps={fps} dims={width}x{height} frames={total}")

    output_path = VIDEOS_DIR / "output.mp4"
    writer = cv2.VideoWriter(
        str(output_path),
        cv2.VideoWriter_fourcc(*"mp4v"),
        fps,
        (width, height),
    )

    frames_seen = defaultdict(int)
    label_for = {}

    tracker_path = Path(ultralytics.__file__).parent / "cfg" / "trackers" / "bytetrack.yaml"
    with open(tracker_path) as f:
        tracker_cfg = yaml.safe_load(f)
    tracker_cfg["track_high_thresh"] = 0.1
    tracker_cfg["track_low_thresh"] = 0.05
    tracker_cfg["new_track_thresh"] = 0.1
    tracker_cfg["match_thresh"] = 0.9
    args = SimpleNamespace(**tracker_cfg, conf=0.1, iou=0.3, max_det=300, frame_rate=int(fps))
    tracker = BYTETracker(args)

    for frame_idx in range(total):
        ok, frame = cap.read()
        if not ok:
            break

        result = model.predict(frame, verbose=False, conf=0.1)[0]
        boxes = result.boxes

        if boxes is not None and len(boxes) > 0:
            tracks = tracker.update(boxes, frame)
            if tracks is not None and len(tracks) > 0:
                for track in tracks:
                    tid = int(track[4])
                    cls_id = int(track[5]) if len(track) > 5 else 0
                    frames_seen[tid] += 1
                    label_for[tid] = model.names[cls_id]

        writer.write(result.plot())
        if frame_idx % 30 == 0:
            print(f"frame {frame_idx}/{total} | tracks: {len(tracks) if tracks is not None else 0}")

    cap.release()
    writer.release()

    # Re-encode to browser-compatible h264
    reencoded_path = VIDEOS_DIR / "output_final.mp4"
    subprocess.run([
        "ffmpeg", "-y",
        "-i", str(output_path),
        "-vcodec", "libx264",
        "-crf", "23",
        "-preset", "fast",
        str(reencoded_path)
    ], check=True)

    print("frames_seen:", dict(frames_seen))
    print("label_for:", label_for)

    tracks = [
        {
            "track_id": tid,
            "time_on_screen_s": round(count / fps, 2),
            "label": label_for[tid],
        }
        for tid, count in frames_seen.items()
    ]   
    print("Output video saved to" f"http://localhost:8000/videos/output.mp4?t={int(time.time())}")


@app.post("/track")
def start_track(video: UploadFile = File(...)):
    (VIDEOS_DIR / "input.mp4").write_bytes(video.file.read())
    run_track_job()
    return {
        "status": "done",
        # "video_url": f"http://localhost:8000/videos/output_final.mp4?t={int(time.time())}",
        # "tracks": tracks,
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)