# Fixing FFmpeg Flickering and Ghosting in TileClipper Output

## What Went Wrong

After running the TileClipper pipeline, the final video had two annoying visual issues:

1. **Flickering**: tiles would quickly switch on and off between 0.5-second segments
2. **Ghosting**: moving objects like cars looked duplicated or stuttered at segment boundaries

The root cause was a recent FFmpeg change that disrupted the temporal dependency between segments.

## What Fixed It

The practical fix, suggested by Prof. Bhattacharya and Shubham, was simple:

1. Dump frames from all of the video segments and re-encode them as one continuous video
2. Drop the first frame from each segment while doing that, which avoids the decoder lag that was causing the flicker

## Automated Fix Script

```bash
#!/bin/bash
# fix_tileclipper_output.sh
# Fixes flickering and ghosting in TileClipper output

SEGMENTS_DIR="removedTileMp4/AITr5S1C4_"
FRAMES_DIR="temp_frames"
OUTPUT_FILE="final_output.mp4"
SEGMENT_DURATION=0.5
FPS=25
FRAMES_PER_SEG=$((FPS * SEGMENT_DURATION / 1))  # frames per 0.5s segment = 12 or 13

# Step 1: Aggregate tiled segments
gpac -i "${SEGMENTS_DIR}/track.mp4" tileagg -o aggregated.mp4

# Step 2: Create temp frames directory
mkdir -p $FRAMES_DIR

# Step 3: Extract frames from each segment, skip first frame
seg_count=0
frame_index=0

for seg in ${SEGMENTS_DIR}/set_*.mp4; do
    # Dump all frames from this segment
    ffmpeg -i "$seg" -q:v 2 "$FRAMES_DIR/seg${seg_count}_frame_%04d.jpg" -y 2>/dev/null
    
    # Skip the first frame (0-th frame) to bypass decoder-lag flicker
    for f in "$FRAMES_DIR"/seg${seg_count}_frame_*.jpg; do
        filename=$(basename "$f")
        frame_num=$(echo "$filename" | grep -oP '\d+(?=\.jpg)')
        
        if [ "$frame_num" -gt 1 ]; then
            # Copy frames after the first one, with sequential numbering
            frame_index=$((frame_index + 1))
            cp "$f" "$FRAMES_DIR/final_frame_$(printf '%05d' $frame_index).jpg"
        fi
    done
    
    seg_count=$((seg_count + 1))
done

# Step 4: Re-encode clean frames into a single continuous video
ffmpeg -framerate $FPS -i "$FRAMES_DIR/final_frame_%05d.jpg" -c:v libx265 -pix_fmt yuv420p $OUTPUT_FILE

echo "Done! Output: $OUTPUT_FILE"
echo "Total segments processed: $seg_count"
echo "Total frames (after dropping first of each segment): $frame_index"

## Results

Before the fix, the output had visible flickering and ghosting.
After the fix, the video played cleanly without those artifacts.

Dataset used: AITr5S1C4_ 
Frames after extraction: 4228
