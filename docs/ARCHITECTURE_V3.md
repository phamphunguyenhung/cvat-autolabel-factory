# Architecture V3 — Object-First Panoptic Annotation Harness

## 1. Design Thesis

The prior CVAT annotation pipeline treated **Things**, **Stuff**, and **Thin Geometric Structures** as a single polygon-generation problem (argmax semantic segmentation + morphological close + polygon simplification + late fixup rules). V3 replaces that monolith with a **Task-Aware Panoptic Harness** (`harness/`) tailored to CPU-first Windows execution (`<= 15.8 GB` RAM, single-heavyweight residency).

```
CVAT Job / Local Frames / Ruleset Schema
                 │
                 ▼
      ┌──────────────────────┐
      │     FrameProfiler     │  Luma (day/night), glare, blur, continuity check
      └──────────┬───────────┘
                 ▼
      ┌──────────────────────┐
      │      LabelRouter      │  Maps schema labels -> THING / STUFF / STRUCTURE / DERIVED_AREA
      └──────────┬───────────┘
                 ▼
   ┌────────────────────────────────────────────────────────────┐
   │                ModelRegistry (CPU Memory Guard)             │
   │  Enforces <= 1 heavyweight model in RAM via unload()+gc()  │
   └────────────────────────────────────────────────────────────┘
        │                       │                       │
        ▼ (Stage 1)             ▼ (Stage 2)             ▼ (Stage 3)
  ┌───────────┐           ┌───────────┐           ┌───────────┐
  │ThingEngine│           │StuffEngine│           │Structure  │
  │OV/YOLO-seg│           │SegFormerB2│           │Engine     │
  │+Crop SAM2 │           │Probs + RLE│           │Lines/Polys│
  └─────┬─────┘           └─────┬─────┘           └─────┬─────┘
        └───────────────┬───────┴───────────────────────┘
                        ▼ (Stage 4: Optional if sequence continuous)
             ┌─────────────────────┐
             │ TemporalAssociation │  ByteTrack / BoT-SORT / OptFlow+Hungarian
             └──────────┬──────────┘
                        ▼
             ┌─────────────────────┐
             │    LayerComposer     │  Raw RLE vs Visible RLE, Z-order, occlusion, derived areas
             └──────────┬──────────┘
                        ▼
             ┌─────────────────────┐
             │QualityEval + ReviewQ │  Metrics, stop gates, prioritized risky-region HTML/JSON
             └──────────┬──────────┘
                        ▼
             ┌─────────────────────┐
             │     CvatAdapter      │  Local SQLite ShapeStore sandbox; explicit --yes for remote
             └─────────────────────┘
```

## 2. Core Architectural Guarantees

1. **Sequential Single-Heavyweight Lifecycle:** Detector -> `unload()+gc()` -> Instance Mask / SAM Crop Refiner -> `unload()+gc()` -> Stuff Probability Segmenter -> `unload()+gc()`. Peak RSS stays safely inside laptop RAM margins.
2. **Pixel-First Internal Representation:** Semantic and instance masks travel through all internal stages as compact **NumPy/JSON COCO-style uncompressed RLE** (`raw_rle`, `visible_rle`), delaying optional CVAT polygon conversion strictly to the export adapter after validation.
3. **Never Auto-Merge Adjacent Instances:** Touching `car` or `pedestrian` masks remain separate `InstanceCandidate` objects separated by detection proposals + negative neighbor prompts when refined.
4. **Honest Conditional Tracking:** `TemporalAssociationEngine` is gated by explicit frame-sequence continuity (`continuity != none` AND measured cross-frame histogram/flow coherence). On snapshots like Job 285, tracking stays OFF.
5. **Conservative Ambiguity Handling:** Low-confidence detections, boundary conflicts, and heavy overlaps enter `ReviewQueue` with evidence rather than being erased or over-smoothed into fake perfection.

## 3. Package Layout (`harness/`)

- `harness/contracts.py`: Typed dataclasses, enums, RLE codecs, serialization helpers.
- `harness/frame_profiler.py`: Luma, glare/saturation, contrast/blur, sequence continuity profiler.
- `harness/label_router.py`: Schema classifier (`THING`/`STUFF`/`STRUCTURE`/`DERIVED_AREA`) and model routing policy.
- `harness/model_registry.py`: CPU memory-guarded sequential registry extending `cvat_tools.core.model_registry.ModelRegistry`.
- `harness/thing_engine.py`: P0 multi-scale OpenVINO/YOLO detector + night enhancement + specialist traffic light/sign cues + `yolo-seg` / crop `SAM 2.1` refinement + duplicate suppression.
- `harness/stuff_engine.py`: P1 probability-map SegFormer-B2 / challenger fusion, component-preserving boundary refinement, independent road fallback, clean polygon export.
- `harness/structure_engine.py`: Lane / crosswalk / curb / pole geometry extraction with glare-streak rejection.
- `harness/temporal_engine.py`: Conditional ByteTrack / BoT-SORT / Optical Flow + Hungarian association.
- `harness/layer_composer.py`: Deterministic Z-order & raw-vs-visible mask arbitration + derived drivable areas.
- `harness/quality_evaluator.py`: Thing, Stuff, Structure, Tracking, System & Stop-Gate evaluator.
- `harness/review_queue.py`: Local HTML visual inspector & prioritized risky-region JSON queue.
- `harness/cvat_adapter.py`: Read-only by default CVAT + SQLite `ShapeStore` adapter with dry-run/backup/rollback.
- `harness/experiment_registry.py`: JSON experiment logger for hypothesis-driven iterations.
- `harness/orchestrator.py`: End-to-end execution stages (`audit`, `thing`, `stuff`, `structure`, `track`, `compose`, `eval`, `preview`, `export`).
