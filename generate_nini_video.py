"""
generate_nini_video.py
======================
Generates 4 video clips (4s each) based on Nini's storyboards using Veo 3.1,
polls until complete, downloads shot1.mp4 ~ shot4.mp4,
concatenates them into nini_final_16s.mp4.

Story: Nini the calico cat barista (16 seconds total):
  Shot 1 (0-4s):  Card payment confirmation
  Shot 2 (4-8s):  Pouring coffee, eyes drifting to milk jug
  Shot 3 (8-12s): Can't resist — sneaks a sip of milk
  Shot 4 (12-16s): Pretends nothing happened, serves coffee with guilty smile
"""

import os
import sys
import time
import requests
from google import genai
from google.genai import types

# Fix console encoding
if sys.stdout.encoding != 'utf-8':
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', encoding='utf-8', errors='replace')
    sys.stderr = os.fdopen(sys.stderr.fileno(), 'w', encoding='utf-8', errors='replace')

API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable not set.")

client = genai.Client(api_key=API_KEY)
out_dir = r"c:\Users\lsyan\Documents\Code\CatAnimation"

SHOT_CONFIGS = [
    {
        "output_name": "shot1.mp4",
        "image_path": os.path.join(out_dir, "storyboards", "shot1_20260904_215307.png"),
        "prompt": """Photorealistic 3D animation, 4 seconds. Cozy warm cafe interior.
The cat barista holds a POS card reader toward the camera with its right paw.
A credit card taps the device. The green screen light flashes with confirmation.
The cat nods gently with a professional friendly smile, then slowly places the POS machine down on the far-left corner of the counter.
Smooth subtle cinematic camera motion. Warm golden ambient cafe lighting.""",
    },
    {
        "output_name": "shot2.mp4",
        "image_path": os.path.join(out_dir, "storyboards", "shot2_20260904_215331.png"),
        "prompt": """Photorealistic 3D animation, 4 seconds. Continuation from Shot 1.
The cat barista tilts the Moka pot to pour dark espresso into the white ceramic mug.
While pouring, the cat's eyes drift sideways toward the small milk jug on the counter with a longing, tempted expression.
The cat's cheeks flush slightly with inner conflict between duty and desire.
Smooth subtle cinematic motion. Warm golden cafe lighting.""",
    },
    {
        "output_name": "shot3.mp4",
        "image_path": os.path.join(out_dir, "storyboards", "shot3_20260904_215351.png"),
        "prompt": """Photorealistic 3D animation, 4 seconds. Continuation from Shot 2.
The cat leans forward and sneaks a sip from the milk jug — unable to resist any longer.
Eyes close slowly in pure bliss. A tiny drop of white milk appears on the pink nose and the corner of the mouth.
The cat's shoulders hunch in slightly, as if hoping nobody saw. Blushing cheeks, a suppressed happy smile.
Smooth cinematic motion. Warm golden cafe lighting.""",
    },
    {
        "output_name": "shot4.mp4",
        "image_path": os.path.join(out_dir, "storyboards", "shot4_20260904_215409.png"),
        "prompt": """Photorealistic 3D animation, 4 seconds. Continuation from Shot 3. Final shot.
The cat quickly straightens up, resumes professional posture, eyes open wide with a warm sweet smile.
The cat lifts the white ceramic mug with heart latte art with both paws and gently extends it toward the viewer.
Eyes twinkle with cheerful, slightly sheepish warmth — hoping the customer didn't notice the sneaky milk sip.
Smooth gentle cinematic motion. Warm golden cafe lighting.""",
    },
]

print("==================================================")
print("Submitting Veo 3.1 video generation tasks...")
print("==================================================")

operations = []
for shot in SHOT_CONFIGS:
    name = shot["output_name"]
    img_path = shot["image_path"]
    prompt = shot["prompt"]

    print(f"Submitting {name} using image: {os.path.basename(img_path)}...")
    image_input = types.Image.from_file(location=img_path)
    op = client.models.generate_videos(
        model="veo-3.1-fast-generate-preview",
        prompt=prompt,
        image=image_input,
    )
    print(f"  [SUBMITTED] {name} -> {op.name}")
    operations.append((name, op.name))

print("\n==================================================")
print("Polling and downloading video clips...")
print("==================================================")

completed = set()
start_time = time.time()

while len(completed) < len(operations):
    for filename, op_name in operations:
        if filename in completed:
            continue

        url = f"https://generativelanguage.googleapis.com/v1beta/{op_name}?key={API_KEY}"
        try:
            res = requests.get(url).json()
            if res.get("done"):
                print(f"  [DONE] {filename}")
                if "response" in res and "generateVideoResponse" in res["response"]:
                    samples = res["response"]["generateVideoResponse"].get("generatedSamples", [])
                    if samples:
                        video_uri = samples[0]["video"]["uri"]
                        video_res = requests.get(f"{video_uri}&key={API_KEY}")
                        save_path = os.path.join(out_dir, filename)
                        with open(save_path, "wb") as f:
                            f.write(video_res.content)
                        print(f"  [SAVED] {filename} ({len(video_res.content)} bytes) -> {save_path}")
                        completed.add(filename)
                elif "error" in res:
                    print(f"  [ERROR] {filename}: {res['error']}")
                    completed.add(filename)
            else:
                elapsed = int(time.time() - start_time)
                print(f"  [WAITING] {filename} is still rendering... ({elapsed}s elapsed)")
        except Exception as e:
            print(f"  [WARN] Exception checking {filename}: {e}")

    if len(completed) < len(operations):
        time.sleep(15)

print("\n==================================================")
print("All video clips downloaded! Now run concat_videos.py to create nini_final_16s.mp4")
print("==================================================")
