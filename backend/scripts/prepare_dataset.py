"""Prepare raw images for YOLO training.

Converts a folder of images into YOLO format with train/val/test splits.
Creates the required directory structure and data.yaml file.

Example:
    python scripts/prepare_dataset.py \\
        --input data/captured \\
        --output data/dataset \\
        --train-ratio 0.7 \\
        --val-ratio 0.2
"""
import argparse
import shutil
from pathlib import Path
import random

import yaml


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True,
                        help="Input directory with raw images")
    parser.add_argument("--output", required=True,
                        help="Output directory for YOLO dataset")
    parser.add_argument("--train-ratio", type=float, default=0.7,
                        help="Ratio of images for training (0-1)")
    parser.add_argument("--val-ratio", type=float, default=0.2,
                        help="Ratio of images for validation (0-1)")
    parser.add_argument("--classes", nargs="+", default=["salamander"],
                        help="Class names")
    args = parser.parse_args()

    input_dir = Path(args.input)
    output_dir = Path(args.output)
    
    if not input_dir.exists():
        raise SystemExit(f"Input directory not found: {input_dir}")

    # Create output structure
    for split in ["train", "val", "test"]:
        (output_dir / "images" / split).mkdir(parents=True, exist_ok=True)
        (output_dir / "labels" / split).mkdir(parents=True, exist_ok=True)

    # Get all image files
    image_files = sorted(list(input_dir.glob("*.jpg")) + list(input_dir.glob("*.png")))
    if not image_files:
        raise SystemExit(f"No images found in {input_dir}")

    print(f"Found {len(image_files)} images")

    # Shuffle and split
    random.shuffle(image_files)
    train_count = int(len(image_files) * args.train_ratio)
    val_count = int(len(image_files) * args.val_ratio)

    train_files = image_files[:train_count]
    val_files = image_files[train_count:train_count + val_count]
    test_files = image_files[train_count + val_count:]

    # Copy files
    splits = {
        "train": train_files,
        "val": val_files,
        "test": test_files
    }

    for split, files in splits.items():
        for src in files:
            dst = output_dir / "images" / split / src.name
            shutil.copy2(src, dst)
            # Create empty label file (user will fill these in with Label Studio)
            label_file = output_dir / "labels" / split / src.stem
            label_file.with_suffix(".txt").touch()
        print(f"  {split}: {len(files)} images")

    # Create dataset.yaml
    dataset_config = {
        "path": str(output_dir.absolute()),
        "train": "images/train",
        "val": "images/val",
        "test": "images/test",
        "nc": len(args.classes),
        "names": {i: name for i, name in enumerate(args.classes)}
    }

    yaml_path = output_dir / "dataset.yaml"
    with open(yaml_path, "w") as f:
        yaml.dump(dataset_config, f, default_flow_style=False)

    print(f"\nDataset prepared!")
    print(f"  Output directory: {output_dir}")
    print(f"  Config file: {yaml_path}")
    print(f"\nNext step: Label your images using Label Studio or manually")
    print(f"  Label file format: class_id x_center y_center width height")
    print(f"  (Coordinates are normalized 0-1)")


if __name__ == "__main__":
    main()
