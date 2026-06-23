# Key Takeaways — Prof. Arani Bhattacharya's Talk

Notes from the presentation “Tiles: Exploring a Hidden Codec Feature for Better Video Streaming” at the IITD × IIITD Video Analytics Workshop, June 13, 2026.

---

## The Big Idea

HEVC tiles were originally built to help decoders run in parallel on multi-core machines. What the research community later realized is that the same feature can be used for something very different: reducing how much video data needs to be sent in the first place.

## Three Systems, Same Core Trick

### MOSAICS for 360° Video

360° video is expensive to stream. It can take roughly 8x more bandwidth than regular video because the system has to cover the full sphere, even though the user only looks at a small part of it at any moment.

MOSAICS uses a DNN to predict which tiles the user is likely to view. It looks at three kinds of signals: head movement, saliency, and motion maps. The work is split into two parts: offline preprocessing that can be shared across users, and live processing that adapts to each viewer in real time.

That split matters. The offline stage gives a good prior from general user behavior, and the live stage sharpens it using the current user’s head movement. The QoE model also includes a penalty for spatial quality changes, since users notice when the viewport looks uneven. In the end, MOSAICS beats FLARE, which used a simpler linear regression approach.

### TileClipper for Traffic Surveillance

TileClipper takes a different angle. In surveillance, the interesting question is not “what looks best to a human?” but “which parts of the scene actually matter to the machine?”

The key observation is that tile bitrate correlates strongly with moving objects, with Spearman correlation in the 0.75–0.90 range. That means you can often tell whether a tile is useful just by looking at how many bits it needs. No GPU is required, there is no re-encoding, and the camera does not need raw pixel access. In practice, the system can even run with a Raspberry Pi attached to the camera.

TileClipper calibrates itself once using percentile statistics, and it stays stable even when weather or lighting changes. It uses F2 because surveillance systems care more about recall than precision. The end result is the same accuracy and savings as GPU-based baselines, but at a much lower compute cost. In live deployment, it delivered about 50% bandwidth savings over 4G.

### COMPACT for Online Classes

COMPACT applies the same tile idea to online learning. Here, the trick is to combine bandwidth from multiple user devices, such as a phone and a laptop.

The system splits the video into foreground and background tiles and sends them over two paths. Since the foreground and background content are largely uncorrelated, out-of-order rendering is acceptable — for example, FG2 followed by BG1 still looks fine. The visual cost is modest: VMAF drops by only about 8%, while end-to-end lag and stall improve by roughly 28%.

## What Stands Out

1. A codec feature can outlive its original purpose. Tiles were meant for parallelism, but they became useful for bandwidth optimization.
2. Existing signals are often enough. Tile bitrate is a free cue, so you do not need extra hardware to get value out of it.
3. Lower compute can beat higher compute when the accuracy is the same. That matters even more at scale.
4. Percentile-based thresholds are more robust than raw bitrate thresholds when conditions change.
5. It helps to split work carefully: do the heavy lifting offline and keep the live path lightweight.

## Q&A Notes

- Codecs are still expected to stay human-readable for the foreseeable future. Neural codecs are progressing, but adoption is slow because they are harder to deploy and do not yet have the same hardware support.
- YouTube still uses a classic approach: pre-encode multiple quality levels, probe the bandwidth from time to time, and choose the best option that fits the constraint.
- Smartphones usually rely on dedicated hardware decoder blocks rather than GPUs.
- Privacy came up as an important concern. The broader point was that researchers should build privacy-preserving systems, especially for applications like traffic surveillance.