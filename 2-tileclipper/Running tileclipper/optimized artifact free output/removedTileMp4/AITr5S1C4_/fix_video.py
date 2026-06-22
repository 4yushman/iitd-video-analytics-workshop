import os
import subprocess
import glob
import shutil

# --- CONFIGURATION ---
# Target pattern for tiled segments with removed tiles
INPUT_PATTERN = "output*_tiled_tile_removed.mp4"
FRAME_TEMP_DIR = "temp_frames"
OUTPUT_VIDEO = "final_smooth_video.mp4"
FRAME_RATE = 30  # Standard frame rate for output

def fix_video():
    # Prepare a clean workspace for individual frames
    if os.path.exists(FRAME_TEMP_DIR):
        shutil.rmtree(FRAME_TEMP_DIR)
    os.makedirs(FRAME_TEMP_DIR)

    # Sort segments numerically to preserve the video sequence
    segments = sorted(glob.glob(INPUT_PATTERN))
    
    if not segments:
        print("Error: No files found matching the specified pattern.")
        return

    print(f"Total {len(segments)} segments identified. Starting optimization...")
    global_frame_count = 0

    for i, seg in enumerate(segments):
        print(f"[{i+1}/{len(segments)}] Processing: {seg}")
        
        # Local temporary workspace for the current segment
        seg_temp = "seg_temp"
        agg_mp4 = "temp_agg.mp4"
        
        if os.path.exists(seg_temp): 
            shutil.rmtree(seg_temp)
        os.makedirs(seg_temp)

        try:
            # STEP A: Normalize the tiled video using GPAC's tileagg
            # This makes the video standard enough for FFmpeg to decode without errors.
            subprocess.run([
                "gpac", "-i", seg, "tileagg", "-o", agg_mp4
            ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            # STEP B: Extract frames from the aggregated segment
            subprocess.run([
                "ffmpeg", "-i", agg_mp4, 
                "-start_number", "0",
                os.path.join(seg_temp, "f_%04d.png")
            ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            # Retrieve and sort extracted frames
            frames = sorted(glob.glob(os.path.join(seg_temp, "*.png")))

            if len(frames) > 1:
                # IMPLEMENTATION OF THE ARANI-CHAUDHARY FIX:
                # We skip the 0-th frame of each segment to bypass the decoder-lag flicker
                # introduced in recent FFmpeg/HEVC processing.
                for f_path in frames[1:]:
                    new_name = f"frame_{global_frame_count:06d}.png"
                    shutil.move(f_path, os.path.join(FRAME_TEMP_DIR, new_name))
                    global_frame_count += 1
            
        except Exception as e:
            print(f"Error encountered while processing {seg}: {e}")
        
        # Cleanup temporary intermediate files to manage storage
        if os.path.exists(agg_mp4): 
            os.remove(agg_mp4)
        shutil.rmtree(seg_temp)

    print(f"\nSuccessfully extracted {global_frame_count} clean frames. Generating final video...")

    # STEP C: Compile all optimized frames back into a single continuous video
    subprocess.run([
        "ffmpeg", "-y",
        "-framerate", str(FRAME_RATE),
        "-i", os.path.join(FRAME_TEMP_DIR, "frame_%06d.png"),
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        OUTPUT_VIDEO
    ], check=True)

    print(f"\nOptimized video saved as: {os.getcwd()}/{OUTPUT_VIDEO}")

if __name__ == "__main__":
    fix_video()