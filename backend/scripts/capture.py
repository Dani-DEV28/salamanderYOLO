"""Capture images from webcam for training dataset.

Press SPACE to save a frame, Q to quit. Frames land in data/captured/ .

Aim for at least 30 images. Variety matters more than quantity. Capture from:
- Multiple angles (5+)
- Different distances (close, mid, far)
- Different lighting conditions
- Different backgrounds
- Different frame positions
"""
import argparse
from pathlib import Path

import cv2


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--camera", type=int, default=0,
                        help="Webcam index")
    parser.add_argument("--output", default="data/captured",
                        help="Output directory for captured images")
    args = parser.parse_args()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    cap = cv2.VideoCapture(args.camera)
    if not cap.isOpened():
        raise RuntimeError(f"Failed to open camera {args.camera}")

    frame_count = len(list(output_dir.glob("*.jpg")))
    print(f"Capturing to {output_dir}")
    print(f"Current frame count: {frame_count}")
    print("Press SPACE to save, Q to quit")

    while True:
        ok, frame = cap.read()
        if not ok:
            break

        cv2.imshow("Capture (SPACE=save, Q=quit)", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord(" "):
            frame_count += 1
            filename = output_dir / f"frame_{frame_count:04d}.jpg"
            cv2.imwrite(str(filename), frame)
            print(f"Saved {filename}")
        elif key in (ord("q"), 27):
            break

    cap.release()
    cv2.destroyAllWindows()
    print(f"Done. Saved {frame_count} frames to {output_dir}")


if __name__ == "__main__":
    main()
