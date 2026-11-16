# CVAT Engineering Toolkit (CET)

Workspace chung cho công cụ CVAT (Day 3 segmentation, Day 4 pose, Day 5 MOT). Ưu tiên Day 5 (MOT17-09, P1-P5).
`week01/` và `guides/` là nháp/metrics cũ, **không bị đụng**.

## Cài và chạy
```powershell
cd D:\06-Learning\AIA-VINGROUP\learning\cvat
pip install -e . --no-deps          # cần sẵn: requests numpy pyyaml opencv ultralytics (openvino/onnxruntime tùy backend)
copy .env.example .env              # CVAT_PAT (hoặc dùng sẵn tools\mot-track-manager\.env làm fallback)
python -m cvat_tools doctor
python -m cvat_tools tools list
python -m cvat_tools --json tools info segmentation.prelabel
python -m cvat_tools projects list
python -m cvat_tools models list
python -m cvat_tools store capture --job 285
python -m cvat_tools store push --job 285          # dry-run mặc định; thêm --yes để ghi
python -m cvat_tools store rollback --latest --job 285
python -m cvat_tools full-bbox --job 285 --open
python -m cvat_tools inspect --project day05-mot17                # chỉ đọc
python -m cvat_tools track assist --project day05-mot17           # manual-assist, không cần AI, chỉ đọc
python -m cvat_tools detect --project day05-mot17 --profile balanced --limit 60 --allow-ai-draft
python -m cvat_tools track bench --project day05-mot17 --limit 60 --allow-ai-draft
python -m cvat_tools track keyframes --project day05-mot17 --tracker bytetrack --limit 60 --allow-ai-draft
python -m cvat_tools track review --project day05-mot17 --limit 60 --allow-ai-draft
python -m mtm check --job 15                                      # wrapper tương thích
python -m pytest -q tests
```

## Cấu trúc
- `src/cvat_tools/core`: client (mặc định chỉ đọc), transactions (backup/run log/rollback), cache theo nội dung, config.
- `src/cvat_tools/detection`: detector lazy-load (pytorch/onnx/openvino), detection cache, độ phân giải thích ứng.
- `src/cvat_tools/tracking`: geometry (từ mtm.core), keyframe optimizer, engine (tracker trên cache), ReID chọn lọc, writer, draft.
- `src/cvat_tools/quality`: manual-assist, review queue HTML. `benchmark/`: detector, tracker, ablation, figures.
- `src/mtm`: wrapper `python -m mtm` (cùng code với `cvat_tools.tracking`).
- `config/`: cvat.*.yaml, models.yaml, profiles.yaml, tracking.yaml. `projects/<name>/project.yaml`: cấu hình từng bài.
- `segmentation/`, `pose/`, `training/`, `export/`: mới có inventory (xem docs/MIGRATION.md), chưa hợp nhất.

## Luật lab Day 5
`RULES.md` cấm nộp box/track AI sinh như nhãn của mình. Lệnh sinh dự đoán AI cần `--allow-ai-draft`; manual-assist, doctor, inspect,
export, models, projects dùng được luôn. Dự đoán AI luôn gắn `provenance: ai_draft`, tách khỏi nhãn người.
Chi tiết: docs/CVAT_SAFETY.md, docs/DAY05_WORKFLOW.md.
