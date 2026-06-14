# IITD × IIITD Video Analytics Workshop

Workshop held on June 13, 2026 at IIT Delhi campus. This was a collaboration between IIT Delhi and IIIT Delhi.

## About

Hands-on from the Video Analytics Systems workshop. Two main sessions were conducted:

- TRQS/FrameQL — by Abhilash Sharma, Rishab, Satyam (IIT Delhi)
- TileClipper — by Prof. Arani Bhattacharya and team (IIIT Delhi)

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

## Prerequisites

- Docker installed and running (works on Ubuntu, macOS, Windows)
- ~10 GB free disk space (Docker images + sample data)

## Quick Start

### TRQS/FrameQL

docker pull satyamj030/trqs:latest
docker run -d -p 8080:8080 -v $(pwd)/data:/app/data --name frameql satyamj030/trqs:latest

Then open http://localhost:8080

### TileClipper

docker pull adarshiiitd/tileclipper:latest
docker run -it -v $(pwd)/sample:/workspace adarshiiitd/tileclipper:latest

Check the individual READMEs in each folder for detailed steps.

## References

- TileClipper Paper: USENIX ATC 2024 (artifact evaluated)
- Notion Tutorial: https://shubhamchdhary.notion.site/Tutorial-on-Utilizing-Video-Tiles-d1cfd85a25234f4cae7184584bd81587

## Contacts

- Assistant Prof. Abhilash Jindal (IITD): ajinda@cse.iitd.ac.in
- Prof. Arani Bhattacharya (IIITD): arani@iiitd.ac.in
- Shubham Chaudhary (IIITD): shubhamch@iiitd.ac.in
- Adarsh Shukla (IIITD): adarshs@iiitd.ac.in
- Najiya Naj (IIITD): najiyan@iiitd.ac.in
