"""Process video files with YOLO detection.

Outputs:
- Annotated video with bounding boxes
- CSV file with detections per frame

Example:
    python scripts/video_inference.py \\
        --weights runs/detect/run1/weights/best.pt \\
        --input data/videos/sample.mp4 \\
        --output results/sample_annotated.mp4 \\
        --csv results/sample_detections.csv
"""
from __future__ import annotations

import argparse
import csv
from pathlib import Path

import cv2
from ultralytics import YOLO


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--weights", required=True,
                        help="Path to the trained .pt weights file")
    parser.add_argument("--input", required=True,
                        help="Path to input video file")
    parser.add_argument("--output", default=None,
                        help="Path to output annotated video (optional)")
    parser.add_argument("--csv", default=None,
                        help="Path to output CSV with detections (optional)")
    parser.add_argument("--conf", type=float, default=0.5,
                        help="Confidence threshold for detections")
    parser.add_argument("--imgsz", type=int, default=320,
                        help="Inference image size (match training imgsz for best results)")
    parser.add_argument("--skip-frames", type=int, default=1,
                        help="Process every Nth frame (default 1 = every frame)")
    args = parser.parse_args()

    # Validate inputs
    weights_path = Path(args.weights)
    if not weights_path.exists():
        raise SystemExit(f"Weights not found at {weights_path}")

    input_path = Path(args.input)
    if not input_path.exists():
        raise SystemExit(f"Input video not found at {input_path}")

    # Load model
    print(f"Loading model from {weights_path}")
    model = YOLO(str(weights_path))

    # Open video
    print(f"Opening video: {input_path}")
    cap = cv2.VideoCapture(str(input_path))
    if not cap.isOpened():
        raise SystemExit(f"Failed to open video: {input_path}")

    # Get video properties
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    print(f"  Resolution: {width}x{height}")
    print(f"  FPS: {fps}")
    print(f"  Total frames: {total_frames}")

    # Setup output video writer if needed
    out = None
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        out = cv2.VideoWriter(
            str(output_path),
            fourcc,
            fps,
            (width, height)
        )
        print(f"  Output video: {output_path}")

    # Setup CSV writer if needed
    csv_file = None
    csv_writer = None
    if args.csv:
        csv_path = Path(args.csv)
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        csv_file = open(csv_path, "w", newline="")
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([
            "frame", "timestamp", "class_id", "class_name", "confidence",
            "x_min", "y_min", "x_max", "y_max", "x_center", "y_center"
        ])
        print(f"  Output CSV: {csv_path}")

    # Process frames
    frame_idx = 0
    processed_frames = 0
    detections_count = 0

    while True:
        ok, frame = cap.read()
        if not ok:
            break

        # Skip frames if requested
        if frame_idx % args.skip_frames != 0:
            frame_idx += 1
            continue

        timestamp = frame_idx / fps if fps > 0 else 0

        # Run inference
        results = model(frame, conf=args.conf, imgsz=args.imgsz, verbose=False)
        result = results[0]

        # Draw annotations
        annotated = result.plot()
        if out is not None:
            out.write(annotated)

        # Write detections to CSV
        if csv_writer is not None:
            for box in result.boxes:
                class_id = int(box.cls[0])
                class_name = model.names[class_id]
                confidence = float(box.conf[0])
                x_min, y_min, x_max, y_max = map(float, box.xyxy[0])
                x_center = (x_min + x_max) / 2
                y_center = (y_min + y_max) / 2

                csv_writer.writerow([
                    frame_idx, timestamp, class_id, class_name, confidence,
                    x_min, y_min, x_max, y_max, x_center, y_center
                ])
                detections_count += 1

        processed_frames += 1
        frame_idx += 1

        # Progress
        if processed_frames % 30 == 0:
            print(f"  Processed {processed_frames} frames... "
                  f"({100*frame_idx/total_frames:.1f}%)")

    # Cleanup
    cap.release()
    if out is not None:
        out.release()
    if csv_file is not None:
        csv_file.close()

    print(f"\nDone!")
    print(f"  Frames processed: {processed_frames}")
    print(f"  Total detections: {detections_count}")
    if args.output:
        print(f"  Annotated video: {args.output}")
    if args.csv:
        print(f"  Detections CSV: {args.csv}")


if __name__ == "__main__":
    main()
