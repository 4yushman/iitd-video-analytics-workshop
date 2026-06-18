# Script to remove tiles from a bunch of videos
from tqdm import tqdm
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import subprocess as sp

outputPath = "segments/"
Path(outputPath).mkdir(exist_ok=True, parents=True)
for i, file in enumerate(tqdm(list(Path("tiledVideos").iterdir()), desc="Removing Tiles....")):
	# print(str(file))
	sp.run(["MP4Box", "-quiet", "-rem", "4", "-rem", "6", "-rem", "8", "-rem", "10", "-rem", "14", str(file), "-out", outputPath+str(file.stem)+"_tiled.mp4"])

print("Generating Plot....")
sizeUT, sizeT = 0, 0
for p in Path("tiledVideos").iterdir():
	sizeUT += p.stat().st_size/1024
for p in Path(outputPath).iterdir():	
	sizeT += (Path(outputPath)/p.name).stat().st_size/1024

plt.bar([1, 2], [np.mean(sizeUT), np.mean(sizeT)])
plt.grid()
plt.ylabel("Filesize (KB)", fontsize=20)
plt.xticks([1, 2], ["Before\nTile\nRemoval", "After\nTile\nRemoval"], fontsize=20)
plt.yticks(fontsize=26)
plt.tight_layout()
plt.savefig("filesize.png")
