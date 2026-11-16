# Panoptic Layer & Visibility Composition Policy (`harness/layer_composer.py`)

## 1. Fundamental Principles

1. **Separate Semantic Class, Instance ID, Track ID, Raw Extent, Visible Mask, and Z-Order:**
   - Occlusion is a relationship between layers, NOT an excuse to destroy underlying background pixels indiscriminately.
   - `StuffRegion.raw_mask_rle` and `InstanceCandidate.mask_rle` preserve each element's raw estimate.
   - `PanopticElement.visible_mask_rle` captures which pixels remain visible to the camera after front-to-back visibility arbitration.

2. **Schema Z-Order Hierarchy (from `config/rulesets/default.yaml` & `docs/QUY_UOC_VE_CHUNG.md`):**
   - `sky`: `z_order = -9`
   - `building`, `wall`, `fence`, `vegetation`, `terrain`: `z_order = -8`
   - `sidewalk`: `z_order = -7`
   - `pole`: `z_order = -2`
   - `road`: `z_order = -1`
   - `area/direct`, `area/alternative`, `lane/*`, and all Things (`car`, `truck`, `bus`, `train`, `motorcycle`, `bicycle`, `pedestrian`, `rider`, `traffic light`, `traffic sign`): `z_order = 0`

3. **Deterministic Arbitration Priority (Highest to Lowest Precedence for Visible Pixel Ownership):**
   1. Human-locked / schema-enforced constraints (e.g., ego-hood exclusion band).
   2. Validated Thing instances (`car`..`traffic sign`) — ordered small/near before large/distant so a foreground `pedestrian` or close `car` properly occludes a background `truck` or `car`.
   3. Validated Structure markings (`lane/*`, `pole`) over Stuff (`road`, `building`, `sky`), except foreground Thing masks always sit in front of road markings!
   4. `road` (`z = -1`) over background Stuff (`z <= -7`) when probability evidence supports road.
   5. Remaining Stuff layers (`sidewalk > building/wall/fence/vegetation/terrain > sky`) using continuous softmax probability comparison inside contested pixels rather than arbitrary morphology flood-fills.

4. **Occlusion & Export Rules:**
   - If a Thing's raw bbox/mask is covered by foreground Things > `0.15` (15%) or occluded by foreground poles/signs matching schema rules, `occluded=True` is propagated cleanly (`occlusion_ratio` stored in provenance).
   - If image boundary touch <= `4 px`, `truncated=True` is set cleanly.
   - **Road & Drivable Area Coupling:** `road` is exported as an intact semantic polygon underneath vehicles (`occlusion` stays semantic), while `area/direct` and `area/alternative` subtract standing foreground vehicle obstacles and strictly remain subsets of validated `road`.
   - Adjacent `car` instances NEVER merge merely because masks touch.
