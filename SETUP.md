# Setup Guide

System setup for Video Analytics Workshop hands-on sessions.

## Prerequisites

- Docker installed and running
- ~10 GB free disk space
- Ubuntu/Linux, macOS, ya Windows (Docker Desktop)

---

## 1. TRQS/FrameQL Setup

### Step 1: Download Data (~7 GB)
```bash
# Download from Google Drive
# Link: https://drive.google.com/file/d/17y6EmgFWBdgpwfXZndj4_nk_eO2f5tY0/view

# Extract
tar -xzf data.tar.gz
```

Data folder structure:
```
data/
  vzas/          ← VZA databases + frames.json
  frames/        ← Frame images
    S02_c006_yolo11x/
    S02_c007_yolo11x/
    ...
```

### Step 2: Pull Docker Image
```bash
docker pull satyamj030/trqs:latest
```

### Step 3: Run Container
Replace `/absolute/path/to/data` with your actual path:

```bash
docker run -d \
  --name frameql \
  -p 8080:80 \
  -v /absolute/path/to/data:/data \
  satyamj030/trqs:latest
```

### Step 4: Open Dashboard
```
http://localhost:8080
```

### Useful Commands
```bash
# Check logs
docker logs frameql

# Stop container
docker stop frameql && docker rm frameql

# Use different port
docker run -d --name frameql -p 9000:80 -v /path/to/data:/data satyamj030/trqs:latest
# Then open http://localhost:9000
```

---

## 2. TileClipper Setup

### Step 1: Pull Docker Image
```bash
docker pull adarshiiitd/tileclipper:latest
```

### Step 2: Download Sample Video (~182 MB)
```bash
# Download from Google Drive
# Link: https://drive.google.com/file/d/1xxz0UdMstGviPVfa8N8HmSTGxVqCJ-Mk/view

# Extract and keep in sample/ folder
mkdir sample
# Extract zip contents to sample/
```

### Step 3: Run Container
```bash
docker run -it -v $(pwd)/sample:/workspace adarshiiitd/tileclipper:latest
```

---

## Quick Reference

| Tool | Container Name | Port | URL |
|------|---------------|------|-----|
| TRQS/FrameQL | frameql | 8080 | http://localhost:8080 |
| TileClipper | (interactive) | - | Inside container |

---

## Troubleshooting

**TRQS dashboard nahi khul raha?**
```bash
docker logs frameql
# Check if data path is correct
```

**TileClipper container exits immediately?**
```bash
docker run -it -v $(pwd)/sample:/workspace adarshiiitd/tileclipper:latest bash
# Run commands manually inside
```

**Permission denied?**
```bash
sudo usermod -aG docker $USER
# Logout and login again
```