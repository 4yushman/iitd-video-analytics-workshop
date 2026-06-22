# Prof. Arani Bhattacharya — "Tiles: Exploring a Hidden Codec Feature for Better Video Streaming"
### WINGS Lab, IIIT Delhi

These are the key points from the 180-page presentation slides shared by Prof. Bhattacharya.

---

## Video Traffic & QoE

- Video traffic grew from 0.9 EB/year (2015) to 210 EB/year (2025) — a 230-240x increase
- 4G becoming ubiquitous in India (~2016) was a major driver
- QoE metrics for humans: resolution, QP, frame rate, quality changes, latency, PSNR, SSIM, VMAF
- QoE metrics for machines: precision, recall, latency (evolving as queries get more complex)
- Two approaches to handle this: (1) increase network capacity (5G/6G), (2) judiciously reduce data sent

## Video Encoding Basics

- Encoding introduces dependencies between consecutive frames and within frames
- Frames grouped into Segments / Group of Pictures (GoP)
- H.264 (old, still on smartphones), H.265 (most common), AV1/AV2 (evolving)
- Codecs reduce data size by over 100x — raw pixels almost never used

## HEVC Tiles — The Key Feature

- Introduced in H.265 standard (~2012-2013)
- Rectangular spatial blocks with no dependencies across tile boundaries
- Originally designed for parallel encoding/decoding on multi-core processors
- Research community repurposed tiles as a tuning knob to reduce data consumption
- First work was FLARE (Qian et al., All Things Cellular 2016) on 360° video

## Three Applications of Tiles

| System | Application | Venue |
|--------|-------------|-------|
| MOSAICS | 360° video streaming with ML | IEEE TNSM 2021 |
| TileClipper | Lightweight ROI selection for traffic surveillance | USENIX ATC 2024 |
| COMPACT | Content-aware multipath live streaming for online classes | ACM MMSys 2025 |

---

## MOSAICS — 360° Video Streaming

### Problem
- Full 360° requires ~200 Mbps vs ~25 Mbps for viewport — 8x bandwidth of ordinary video
- User only sees 80°-110° out of full 360° sphere

### Prior Work: FLARE
- Encodes video in tiles, fetches viewport tiles at high quality, others at lower or not at all
- Uses linear regression on past viewport movement for 1-2s prediction
- Inaccurate prediction hurts QoE — they fetched conservatively to compensate

### MOSAICS Approach
- DNN-based viewport prediction using 3 modes of data:
  1. User head movement
  2. Saliency (CV models predict viewing direction from color contrast)
  3. Motion map (moving regions attract user attention, e.g., football → users look at ball)
- Architecture: 3D CNN + LSTM + CNN (spatio-temporal)
- Computation split:
  - Pre-processing (offline): video content analysis — common across all users, stored on server
  - Live processing (real-time): user head movement + pre-processed results → probability map (P1…P16 per tile)
- Live processing fast enough: ≤0.7s on cheap GPUs

### QoE Model
- QoE = μ₁·E[Q] − μ₃·V_s − μ₄·V_t − μ₂·E[T]
  - E[Q] = expected quality seen by user
  - V_s = spatial quality change penalty (novel — users dislike seeing quality differences across viewport)
  - V_t = temporal quality change penalty
  - E[T] = additional buffering time
- Becomes a knapsack-like optimization problem: maximize QoE subject to bandwidth constraint
- Per-user optimization, but pre-processing gives prior probability from general user behavior

### Evaluation
- 10 YouTube 360° videos, 1 min each, 4K quality
- 20 users head tracking data (8 train, 12 test)
- Real 4G/LTE network traces
- Baselines: viewport-only, viewport+, FLARE (linear regression), BBA (traditional, fetches all)
- MOSAICS outperforms all baselines including FLARE
- Better prediction + pre-processing = better QoE

### Dataset Size Note
- 10 videos seems small but getting large 360° video datasets was very hard at that time
- Videos were specifically chosen, not meant to generalize to arbitrary videos

---

## TileClipper — Traffic Surveillance

### Problem
- Cameras capture video → send over wireless → cloud server runs DNN
- Bandwidth constrained on wireless networks
- Since machines (not humans) consume the data, can we completely remove irrelevant spatial content?

### Prior Work Limitation
- SIGCOMM/NSDI 2020-21 works filter spatial content but need pixel-level data
- Commercial cameras only give encoded output, not raw pixels
- Integrating filtering logic into camera firmware is impractical

### Key Insight
- Tile manipulation in HEVC/H.265 does not require re-encoding or pixel access
- Just remove entire tiles — tiles are independently encoded, so removal is clean
- Attach a Raspberry Pi to camera (no need to modify camera itself)

### Tile Bitrate as Object Proxy
- Tile bitrate (bits per second per tile) correlates with moving object presence
- Spearman correlation: 0.75–0.90 (strong)
- Intuitive: complex scenes with moving objects → codec uses more bits
- Easy to compute: just probe how much data is written to memory

### Challenges with Bitrate Signal
- Noisy — small spikes occur even without objects (camera shake, background trees, lighting changes)
- Bitrate affected by lighting conditions (changes by ~30%)
- Bitrate differs across tiles (>2x difference) — near tiles have larger objects = larger spikes
- Cannot use a global static threshold

### Calibration (Adaptive Thresholding)
- One-time calibration (~1 min at startup)
- Identify m-th and n-th percentiles of bitrate distribution for tiles with/without objects
- Threshold = midpoint of m and n percentiles
- Runs independently per tile (each has distinct distribution)
- F2 score used to balance precision vs recall (F2 gives 4x weight to recall — surveillance should not miss anything)
- Exhaustive search for best <m, n> pair that maximizes F2 score

### Why No Recalibration?
- Uses percentile statistics, not raw bitrate
- Overall bitrate shifts with weather/lighting but percentile structure preserved
- Exception: if calibration happens when no objects present (e.g., road blocked), secondary strategy handles it

### Evaluation Results
- Baselines: Frame filtering (SIGCOMM '20), quality-adaptive filtering, super-resolution upsampling (HotCloud '19)
- TileClipper accuracy and savings are close to baselines — not better
- Key advantage: way less GPU usage — no re-encoding needed
- Same savings, same accuracy, but at fraction of the compute cost
- Camera-side: works with just a Raspberry Pi
- Live deployment: 5m from road, 4G network, ~50% bandwidth savings, >88% and >55% accuracy/savings metrics
- Artifact evaluated by USENIX ATC reviewers — "results were as advertised"

---

## COMPACT — Online Class Streaming

### Problem
- Online learning growing rapidly (Mobile Learning Market ~4x growth)
- Live streaming for classes needs consistently high bandwidth
- People own multiple devices — can we aggregate bandwidth?

### Key Idea
- Multiple user-end devices contribute bandwidth (e.g., phone + laptop)
- Prior multipath works suffer from Head-of-Line (HoL) blocking — they're content-oblivious
- Split video into Foreground (FG) and Background (BG) tiles, route over two paths
- Allow content to render out-of-order: FG2 + BG1 is acceptable since FG and BG are uncorrelated

### Scheduler Design
- Optimizes utility = w₁·Quality − w₂·InterSegment Quality Switch − w₃·IntraSegment Quality Switch − w₄·Stall
- Weights found via exhaustive search

### Architecture
- FG Detection & Tile Segregation → FG/BG Segment Queues → Scheduler & Streamer → Helper Device → Tile Stitcher + BG Tile Cache
- BG tile cache enables reuse of background content across segments

### Results
- VMAF score degrades only ~8% with out-of-order stitching (visually acceptable)
- ~28% improvement in E2E lag and stall, up to 3.4x improvement over baselines
- Gracefully handles sudden path fluctuations
- Live experiment on 4G networks validates feasibility

---

## Overall Conclusion

Tiles were designed for parallel decoding but became a powerful tool for data reduction:
- MOSAICS: Pre-computed DNN viewport prediction to adapt quality at tile level
- TileClipper: Bitrate-object correlation to filter irrelevant tiles without GPU
- COMPACT: FG/BG uncorrelation to adjust multipath synchronization

Hands-on: `docker pull adarshiiitd/tileclipper:latest`
Contact: arani@iiitd.ac.in