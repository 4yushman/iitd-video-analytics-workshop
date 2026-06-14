# IITD × IIITD Video Analytics Workshop

Workshop held on June 13, 2026 at IIT Delhi campus. This was a collaboration between IIT Delhi and IIIT Delhi.

## About

Hands-on from the Video Analytics Systems workshop. Two main sessions were conducted:

- **TRQS/FrameQL** — by Abhilash Sharma, Rishab, Satyam (IIT Delhi)
- **TileClipper** — by Prof. Arani Bhattacharya and team (IIIT Delhi)

Dr. Shibendu from Amazon Prime Video also gave a talk on adaptive sensing.

## What I Did

### 1. TRQS/FrameQL
- Set up DuckDB-based web dashboard for querying surveillance video data
- Used TrQL query language to run spatio-temporal queries
- Stored trajectories as quadratic polynomials instead of raw bounding boxes
- Ran queries for car detection, stationary vehicles, lane tracking, close pairs, people walking together

### 2. TileClipper
- Encoded video with HEVC tiles using Kvazaar
- Removed unimportant tiles to save bandwidth (~20-25% size reduction)
- Used tile bitrate as proxy for detecting moving objects (no GPU needed)
- Ran heatmap and filesize comparison scripts
- Pipeline: FFmpeg → Kvazaar → MP4Box → GPAC → TileClipper

## Folder Structure

