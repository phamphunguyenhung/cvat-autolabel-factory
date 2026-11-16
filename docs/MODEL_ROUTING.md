# Model Routing Policy V3 (`harness/label_router.py` & `harness/model_registry.py`)

## 1. Hardware Constraints (Baseline)

- CPU: 6 cores / 12 threads, Windows 11, no CUDA GPU.
- Physical RAM: 15.8 GB (~4.5 GB headroom available under desktop load).
- Budget targets per stage (CPU):
  - **Thing Engine (OpenVINO default):** target `<= 5s/frame` day, `<= 7s/frame` night (with CLAHE/tiling).
  - **Stuff Engine (SegFormer-B2 ONNX):** `~3.5s/frame` (`3014 MB` peak RSS solo).
  - **SAM Crop Refiner (`mobile_sam.pt` / `sam2.1_b.pt`):** Invoked **only on ambiguous/overlapping crops**, loaded only after detector unload.
  - **Challenger (`Mask2Former-Swin-L`):** Off in fast default mode (`~10.1s/f` + `19.5s` load); selectable via challenger mode when deep night road quality outweighs latency.

## 2. Label Classification Matrix

| Group | Labels (Job 285 Schema) | Export Shape | Preferred Primary Tool | Secondary / Conditional Tool |
|---|---|---|---|---|
| **THING** | `car`, `truck`, `bus`, `train`, `motorcycle`, `bicycle`, `pedestrian`, `rider`, `traffic light`, `traffic sign` | `rectangle` (CVAT) + internal `mask_rle` | OpenVINO `yolo26l` (1280) / `yolo26s` (960/640) | `yolo26s-seg.pt`, `sam2.1_b.pt` / `mobile_sam.pt` on overlapping/occluded crops; SegFormer sign cue |
| **STUFF** | `road`, `sidewalk`, `sky`, `building`, `wall`, `fence`, `vegetation`, `terrain` | Internal `mask_rle` -> optional simplified `polygon` | `segformer_b2_cityscapes.onnx` softmax probabilities | `facebook/mask2former-swin-large-cityscapes-semantic` (challenger / difficult night road) |
| **STRUCTURE** | `lane/crosswalk`, `lane/single white`, `lane/double white`, `lane/single yellow`, `lane/double yellow`, `lane/road curb`, `pole` | `polygon` (j285) or `polyline` (ruleset-driven) | Classical CV geometry (`lanes/detectors/*` + glare filter + crosswalk rect fit + vertical pole merge) | `8bits-ai/SegFormer-Lane-Marking` (diagnostic cue only — raw IoU 0.01–0.04) |
| **DERIVED_AREA** | `area/direct`, `area/alternative` | `polygon` | Derived from validated `road` mask + ego lane corridor + lane separators + Thing clear zone | Review flag when night `road` confidence < 0.55 |

## 3. Adaptive Frame Routing

`FrameProfiler` inspects each image before routing:
- **Daylight (`mean_luma >= 70.0`):** Single base frame + optional horizon strip for distant traffic lights/signs; skip night CLAHE variants.
- **Night / Low-Light (`mean_luma < 70.0`) or High Glare (`saturated_ratio > 0.015`):**
  - Enable dark-shadow lift / CLAHE detection variant for Thing Engine (`all_objects.py` multi-variant fusion).
  - Activate highlight-glare & streetlamp halo filters on `traffic light` proposals (`luma hotspot`, aspect/halo symmetry checks) and headlight-streak rejection on `lane/*`.
  - Lower threshold ONLY into `review_queue` (`review_conf_floor .. accept_conf`) rather than silent accept or silent discard.
- **Sequence Continuity Gate (`TemporalAssociationEngine`):**
  - Requires `ruleset.continuity != "none"` AND measured median adjacent histogram correlation >= 0.45 across ordered frames.
  - Job 285 (`continuity=none`, `hist_corr ~ 0.01-0.06`): tracking stays **DISABLED** (`tracking_enabled=False`).
