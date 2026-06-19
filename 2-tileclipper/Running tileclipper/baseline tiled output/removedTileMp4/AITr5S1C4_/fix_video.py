import os
import subprocess
import glob
import shutil

# --- CONFIGURATION ---
# Pattern to match the tiled segments where tiles were removed
INPUT_PATTERN = "output*_tiled_tile_removed.mp4"
FRAME_TEMP_DIR = "temp_frames"
OUTPUT_VIDEO = "final_smooth_video.mp4"
FRAME_RATE = 30  # Adjust based on your original video's FPS

def fix_video():
    # Initialize a clean directory for temporary frame storage
    if os.path.exists(FRAME_TEMP_DIR):
        shutil.rmtree(FRAME_TEMP_DIR)
    os.makedirs(FRAME_TEMP_DIR)

    # Fetch and sort segments to maintain temporal order
    segments = sorted(glob.glob(INPUT_PATTERN))
    
    if not segments:
        print("Error: No files matching the pattern were found. Check your directory path.")
        return

    print(f"Successfully found {len(segments)} segments. Initializing optimization pipeline...")
    global_frame_count = 0

    for i, seg in enumerate(segments):
        print(f"[{i+1}/{len(segments)}] Processing segment: {seg}")
        
        # Setup temporary directories for the current segment
        seg_temp = "seg_temp"
        agg_mp4 = "temp_agg.mp4"
        if os.path.exists(seg_temp): shutil.rmtree(seg_temp)
        os.makedirs(seg_temp)

        try:
            # STEP A: Normalize the tiled video using GPAC's tileagg
            # This 'aggregates' tiles into a standard format that FFmpeg can properly decode.
            subprocess.run([
                "gpac", "-i", seg, "tileagg", "-o", agg_mp4
            ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            # STEP B: Extract individual frames from the aggregated segment
            subprocess.run([
                "ffmpeg", "-i", agg_mp4, 
                "-start_number", "0",
                os.path.join(seg_temp, "f_%04d.png")
            ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            # Retrieve extracted frames and sort them
            frames = sorted(glob.glob(os.path.join(seg_temp, "*.png")))

            if len(frames) > 1:
                # Apply the "Arani-Chaudhary Fix": Skip the 0-th frame
                # This bypasses the decoder-lag flicker introduced in recent FFmpeg updates.
                for f_path in frames[1:]:
                    new_name = f"frame_{global_frame_count:06d}.png"
                    shutil.move(f_path, os.path.join(FRAME_TEMP_DIR, new_name))
                    global_frame_count += 1
            
        except Exception as e:
            print(f"Critical error processing {seg}: {e}")
        
        # Clean up intermediate files for this segment to save disk space
        if os.path.exists(agg_mp4): os.remove(agg_mp4)
        shutil.rmtree(seg_temp)

    print(f"\nOptimization complete. {global_frame_count} clean frames ready for encoding.")

    # STEP C: Re-encode the sequence of frames into a single, smooth video
    # Using libx264 for high compatibility across standard media players.
    subprocess.run([
        "ffmpeg", "-y",
        "-framerate", str(FRAME_RATE),
        "-i", os.path.join(FRAME_TEMP_DIR, "frame_%06d.png"),
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        OUTPUT_VIDEO
    ], check=True)

    print(f"\nSuccess! Artifact-free video is ready at: {os.getcwd()}/{OUTPUT_VIDEO}")

if __name__ == "__main__":
    fix_video()