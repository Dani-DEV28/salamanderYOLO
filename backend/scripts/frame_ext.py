import cv2
import os
import sys
import argparse

def process_video(video_path, output_path, interval_seconds=10):
    # 1. Open the video file
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print(f"❌ Error: Could not open video {video_path}")
        return

    # 2. Get metadata
    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps == 0: fps = 30  # Fallback for some codecs
    
    # Calculate frame interval (Java code used frameRate * 10)
    frame_interval = int(fps * interval_seconds)
    
    # Create output directory if it doesn't exist
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    frame_count = 0
    saved_count = 0

    print(f"🚀 Starting extraction: {video_path} at 1 frame every {interval_seconds}s")

    while True:
        ret, frame = cap.read()
        
        # Break loop if no more frames
        if not ret:
            break

        # 3. Extract frame based on interval
        if frame_count % frame_interval == 0:
            filename = os.path.join(output_path, f"frame_{frame_count}.jpg")
            # You can add your color thresholding logic here before saving
            cv2.imwrite(filename, frame)
            saved_count += 1

        frame_count += 1

    cap.release()
    print(f"✅ Extraction complete. Saved {saved_count} frames to '{output_path}'.")

if __name__ == "__main__":
    # 4. Command Line Argument Parsing
    parser = argparse.ArgumentParser(description="Extract frames from video for YOLO training.")
    parser.add_argument("--video", type=str, required=True, help="Path to input video file")
    parser.add_argument("--out", type=str, required=True, help="Path to output directory")
    parser.add_argument("--interval", type=int, default=10, help="Interval in seconds (default: 10)")
    # Included these to match your Java signature, though logic isn't applied above
    parser.add_argument("--hex", type=str, help="Target hex color")
    parser.add_argument("--thresh", type=int, help="Color threshold")

    args = parser.parse_args()

    process_video(args.video, args.out, args.interval)