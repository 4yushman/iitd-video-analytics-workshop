from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import subprocess as sp

video = "video_tiled.mp4"
bitrate = sp.run(["ffprobe", "-v", "error",
								  "-show_entries", "stream=bit_rate",
									"-of", "default=noprint_wrappers=1", 
									video], 
									stdout=sp.PIPE
									)

arr = np.fromiter(map(lambda x: int(x[9:]), bitrate.stdout.decode().split('\n')[1:-1]), dtype=int)          # 9 => 'bit_rate='; [1:-1] => 1 because tile 1 has metadata only
print(arr)
z = np.flip(arr.reshape(4,4), axis=0)
plt.xlabel('Width', fontsize=20)
plt.ylabel('Height', fontsize=20)
c = plt.pcolormesh(range(1, 5), range(1, 5), z, cmap="copper", shading='auto')
cbar = plt.colorbar(c)
cbar.set_label('Bitrate', rotation=270,labelpad=12)
plt.tight_layout()
plt.savefig("heatmap.png")
