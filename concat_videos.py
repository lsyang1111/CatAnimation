import os, sys
from moviepy import VideoFileClip, concatenate_videoclips

out_dir = r"c:\Users\lsyan\Documents\Code\CatAnimation"

# v7: Use shot1/shot2/shot3 if they exist, otherwise fall back to clip1/clip2/clip3
if os.path.exists(os.path.join(out_dir, "shot1.mp4")):
    clip1_path = os.path.join(out_dir, "shot1.mp4")
    clip2_path = os.path.join(out_dir, "shot2.mp4")
    clip3_path = os.path.join(out_dir, "shot3.mp4")
    output_path = os.path.join(out_dir, "nini_final_12s.mp4")
    print("[Nini mode] Using shot1/shot2/shot3 -> nini_final_12s.mp4")
else:
    clip1_path = os.path.join(out_dir, "clip1.mp4")
    clip2_path = os.path.join(out_dir, "clip2.mp4")
    clip3_path = os.path.join(out_dir, "clip3.mp4")
    output_path = os.path.join(out_dir, "final_cat_animation.mp4")
    print("[v1 mode] Using clip1/clip2/clip3 -> final_cat_animation.mp4")

clips_to_concat = []
paths = [clip1_path, clip2_path, clip3_path]

print("Loading and verifying video clips...")
for idx, path in enumerate(paths, 1):
    if not os.path.exists(path):
        print(f"Warning: Clip {idx} ({path}) does not exist.")
        continue
    clip = VideoFileClip(path)
    print(f"Clip {idx} loaded: duration = {clip.duration:.2f}s, resolution = {clip.size}, fps = {clip.fps}")
    clips_to_concat.append(clip)

if not clips_to_concat:
    raise FileNotFoundError("No valid input clips found for concatenation.")

print(f"Concatenating {len(clips_to_concat)} clips...")
final_clip = concatenate_videoclips(clips_to_concat, method="compose")
print(f"Total concatenated duration: {final_clip.duration:.2f}s")

# Write video file with standard h264 and AAC settings
final_clip.write_videofile(
    output_path,
    codec="libx264",
    audio_codec="aac",
    fps=30,
    preset="medium",
    bitrate="8000k"
)
print(f"Successfully saved final video to: {output_path}")

# Close resources
for c in clips_to_concat:
    c.close()
final_clip.close()

