import matplotlib.pyplot as plt
import subprocess as sp
from pathlib import Path
import numpy as np
from tqdm import tqdm

# Setup paths
outputPath = "segments_removed/"
Path(outputPath).mkdir(exist_ok=True, parents=True)
inputPath = Path("tiledVideos")

# 1. Process all videos in the tiledVideos folder
video_files = list(inputPath.glob("*.mp4"))
if not video_files:
    print("Error: No .mp4 files found in 'tiledVideos' folder!")
else:
    for file in tqdm(video_files, desc="Removing Tiles...."):
        output_file = Path(outputPath) / (file.stem + "_removed.mp4")
        # Removing tiles 4, 6, and 8
        sp.run(["MP4Box", "-quiet", "-rem", "4", "-rem", "6", "-rem", "8", str(file), "-out", str(output_file)])

    print("Generating Plot....")
    sizeUT, sizeT = [], []
    for p in inputPath.glob("*.mp4"):
        sizeUT.append(p.stat().st_size / 1024) # Size in KB
        
    # Measure size of processed files
    for p in Path(outputPath).glob("*.mp4"):
        sizeT.append(p.stat().st_size / 1024) # Size in KB

    # 2. Create the comparison bar chart
    plt.figure(figsize=(10, 6))
    plt.bar([1, 2], [np.mean(sizeUT), np.mean(sizeT)], color=['blue', 'green'])
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.ylabel("Average Filesize (KB)", fontsize=15)
    plt.xticks([1, 2], ["Before\nRemoval", "After\nRemoval"], fontsize=12)
    plt.title("Bandwidth Savings via Tile Removal", fontsize=18)
    
    # Save the plot
    plt.savefig("filesize_comparison.png")
    print("Done! Check 'filesize_comparison.png' in your folder.")
