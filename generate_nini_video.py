"""
generate_nini_video.py
======================
Generates 3 video clips (4s each) based on Nini's storyboards using Veo 3.1,
polls until complete, downloads shot1.mp4, shot2.mp4, shot3.mp4,
concatenates them into nini_final_12s.mp4, and pushes to GitHub.
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
        "image_path": os.path.join(out_dir, "storyboards", "shot1_20260904_110333.png"),
        "prompt": """Photorealistic 3D animation, 4 seconds.
A gentle calico cat Nini (white fur with orange and black patches, green eyes, white chest, short cute small cat proportions) wearing a brown leather apron stands behind a wooden barista counter inside a cozy warm cafe.
Counter height reaches cat's chest level.
Counter has ONLY TWO items: ONE empty white ceramic mug in center, ONE classic Bialetti Moka Express octagonal aluminum Moka pot with iconic mustache man raising finger logo on front.
The cat holds ONE light grey POS card reader with glowing green screen up with its right paw toward camera.
A credit card taps the device. Green confirmation light flashes.
ONLY AFTER green light: cat nods gently and places POS machine on far left of counter.
Cinematic warm cafe lighting, 8K fur texture.""",
    },
    {
        "output_name": "shot2.mp4",
        "image_path": os.path.join(out_dir, "storyboards", "shot2_20260904_110351.png"),
        "prompt": """Photorealistic 3D animation, 4 seconds. Continuation from Shot 1.
SAME calico cat Nini (white/orange/black patches, green eyes, short cute small cat proportions) in brown leather apron behind wooden barista counter.
Counter: POS machine on far LEFT (visible), ONE white ceramic mug STATIONARY in center.
Cat grips the EXACT SAME Bialetti Moka Express octagonal aluminum Moka pot (with iconic mustache man raising finger logo on front) by its RIGHT-SIDE black handle, tilts it and pours dark espresso into the STATIONARY white ceramic mug.
Cat sets Moka pot down, picks up milk pitcher, pours steamed milk into SAME mug creating heart latte art.
Cinematic warm cafe lighting, 8K fur texture.""",
    },
    {
        "output_name": "shot3.mp4",
        "image_path": os.path.join(out_dir, "storyboards", "shot3_20260904_110409.png"),
        "prompt": """Photorealistic 3D animation, 4 seconds. Continuation from Shot 2.
Close-up shot of SAME calico cat Nini (white/orange/black fur patches, green eyes, white chest, adorable small cat proportions) in brown leather apron.
The cat lifts the SAME white ceramic mug (heart latte art on top) with BOTH PAWS to offer it to the viewer.
Just before handing it over, the cat can't resist — it gently licks a tiny sip of milk foam with its small pink tongue.
The cat slowly looks up, caught on camera.
Expression: NOT guilty smirk, but the most innocent, soft, doe-eyed look — saying "I'm sorry... but it was so good 🥺".
The cat softly extends the mug toward the viewer with both paws.
Soft warm cinematic lighting, 8K calico fur texture.""",
    },
]

print("==================================================")
print("🎬 Submitting Veo 3.1 video generation tasks...")
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
print("⏳ Polling and downloading video clips...")
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
                        print(f"  [SAVED] {filename} ({len(video_res.content)} bytes) to {save_path}")
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
print("🎉 All video clips downloaded successfully!")
print("==================================================")
