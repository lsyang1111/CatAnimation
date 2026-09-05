import os
from moviepy import VideoFileClip, concatenate_videoclips

out_dir = os.path.dirname(os.path.abspath(__file__))

# 4-shot 16s Nini animation
shot_paths = [
    os.path.join(out_dir, "shot1.mp4"),
    os.path.join(out_dir, "shot2.mp4"),
    os.path.join(out_dir, "shot3.mp4"),
    os.path.join(out_dir, "shot4.mp4"),
]
output_path = os.path.join(out_dir, "nini_final_16s.mp4")
print("[Nini 16s mode] Concatenating shot1/shot2/shot3/shot4 -> nini_final_16s.mp4")

clips_to_concat = []

print("Loading and verifying video clips...")
for idx, path in enumerate(shot_paths, 1):
    if not os.path.exists(path):
        print(f"  [SKIP] Shot {idx} ({os.path.basename(path)}) not found.")
        continue
    clip = VideoFileClip(path)
    print(f"  [OK] Shot {idx}: duration={clip.duration:.2f}s, resolution={clip.size}, fps={clip.fps}")
    clips_to_concat.append(clip)

if not clips_to_concat:
    raise FileNotFoundError("No valid input clips found for concatenation.")

print(f"\nConcatenating {len(clips_to_concat)} clips...")
final_clip = concatenate_videoclips(clips_to_concat, method="compose")
print(f"Total duration: {final_clip.duration:.2f}s")

final_clip.write_videofile(
    output_path,
    codec="libx264",
    audio_codec="aac",
    fps=30,
    preset="medium",
    bitrate="8000k"
)
print(f"\n[SUCCESS] Saved final video: {output_path}")

for c in clips_to_concat:
    c.close()
final_clip.close()
