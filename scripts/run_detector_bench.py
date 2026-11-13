"""Lenh tai lap: python scripts/run_detector_bench.py [--limit 30] -> data/benchmarks/detector_bench.csv
Doan tuan tu MOT17-09 frame 0..limit-1. Moi cau hinh chay trong tien trinh rieng (peak RAM sach)."""
import argparse
from pathlib import Path

from cvat_tools.benchmark.detector_bench import bench
from cvat_tools.core import paths

ap = argparse.ArgumentParser()
ap.add_argument("--limit", type=int, default=30)
ap.add_argument("--frames", default=str(paths.REPO / "day05/labs/K5-L2-MOTTracking/.lab-local/mot17-09"))
ap.add_argument("--only", nargs="*", help="vd yolo26l:pytorch:1920")
a = ap.parse_args()
CONFIGS = [("yolo26l", "pytorch", 1920), ("yolo26l", "pytorch", 640),
           ("yolo26n", "pytorch", 640), ("yolo26n", "onnx", 640), ("yolo26n", "openvino", 640),
           ("yolo26s", "pytorch", 640), ("yolo26s", "onnx", 640), ("yolo26s", "openvino", 640),
           ("yolo26s", "openvino", 960), ("yolo26s", "openvino_fp16", 640)]
if a.only:
    CONFIGS = [tuple(x.split(":")[:2]) + (int(x.split(":")[2]),) for x in a.only]
for m, b, sz in CONFIGS:
    r = bench(m, b, sz, a.frames, 0, a.limit)
    print({k: r.get(k) for k in ("model", "backend", "imgsz", "median_ms", "p95_ms", "fps", "peak_ram_mb", "cpu_load_before", "noisy", "status", "note")}, flush=True)
