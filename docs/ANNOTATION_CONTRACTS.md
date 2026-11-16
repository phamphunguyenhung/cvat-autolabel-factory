# Annotation Contracts V3 (`harness/contracts.py`)

All cross-engine interfaces exchange immutable/explicit typed contracts instead of loose untyped dicts.

## 1. Compact RLE Mask Format (`RleMask`)
- Stored as `{ "size": [height, width], "counts": [run0, run1, ...] }` (row-major alternating `0`/`1` pixel runs in PyTorch/COCO uncompressed C-order or Fortran-order clearly documented — V3 standardizes on **row-major C-order** `arr.reshape(-1)` with helpers `encode_rle(mask)` and `decode_rle(rle)`).
- Fast byte-efficient JSON serialization + exact `IoU`, `area_px`, `bbox`, and `overlap_px` arithmetic without holding many full `H x W` float arrays in RAM.

## 2. Core Data Contracts

1. **`FrameProfile`**:
   - `frame_id`, `width`, `height`, `mean_luma`, `is_night`, `contrast_std`, `glare_ratio`, `blur_score`, `continuity_group`, `metadata`.
2. **`InstanceCandidate`** (Thing Engine output):
   - `candidate_id`, `frame_id`, `label`, `bbox_xyxy`, `conf`, `source_model`, `mask_rle` (optional `RleMask`), `mask_source` (`"none" | "yolo_seg" | "sam_crop" | "bbox_fallback"`), `occluded`, `truncated`, `occlusion_ratio`, `uncertainty`, `status` (`"accepted" | "review" | "suppressed"`), `duplicate_group`, `track_id`, `provenance`.
3. **`StuffRegion`** (Stuff Engine output):
   - `region_id`, `frame_id`, `label`, `raw_mask_rle`, `prob_mean`, `prob_p90`, `boundary_uncertainty`, `component_count`, `simplified_polygon` (validated optional outer boundary `[x1, y1, ...]`), `source_model`, `status`, `provenance`.
4. **`StructureGeometry`** (Structure Engine output):
   - `structure_id`, `frame_id`, `label`, `geometry_type` (`"polygon" | "polyline" | "mask"`), `points`, `mask_rle`, `conf`, `continuity_score`, `glare_risk`, `source_model`, `status`, `provenance`.
5. **`TrackState`** (Temporal Engine output — conditional):
   - `track_id`, `label`, `state` (`"tentative" | "confirmed" | "occluded" | "lost" | "terminated"`), `history` (`{frame_id: candidate_id}`), `velocity_xy`, `last_seen_frame`, `reid_events`, `interpolated_frames`.
6. **`PanopticElement`** & **`ComposedScene`** (Layer Composer output):
   - Distinguishes `raw_mask_rle` (unoccluded semantic/instance estimate) vs `visible_mask_rle` (visible pixels after higher `z_order` visibility resolution), alongside `z_order`, `occluded_by` IDs, `occlusion_ratio`, `review_flags`, and CVAT export shapes.
7. **`ReviewItem`** (`ReviewQueue` output):
   - `frame_id`, `element_id`, `label`, `priority_score`, `reason_code`, `message`, `bbox_xyxy`, `evidence`.
8. **`ExperimentRecord`** (`ExperimentRegistry` output):
   - `experiment_id`, `timestamp`, `hypothesis`, `baseline_id`, `config`, `metrics`, `latency_s_per_frame`, `peak_rss_mb`, `verdict` (`"accept" | "reject" | "inconclusive"`), `notes`.
