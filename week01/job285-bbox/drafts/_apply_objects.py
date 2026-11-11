import sys; sys.path.insert(0,'src'); sys.path.insert(0,'scripts')
from collections import Counter
from cvat_seg.cli import get_adapter
from draftstore import load_draft, save_draft, apply_shapes
KEEP={"car","truck","bus","motorcycle","bicycle","pedestrian","rider","traffic light","train","traffic sign"}
d=load_draft(285,"bboxall")
sel=[{k:v for k,v in s.items() if not k.startswith("_")} for s in d["shapes"] if s["_label"] in KEEP]
save_draft(285,"bboxobj",{"shapes":sel})
ad=get_adapter()
apply_shapes(ad,285,sel,"bboxobj")
after=ad.get_annotations(285); L={l["id"]:l["name"] for l in ad.get_job_labels(285)}
print(Counter(L[s["label_id"]] for s in after["shapes"]), Counter(s["source"] for s in after["shapes"]))
