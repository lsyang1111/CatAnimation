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
        "image_path": os.path.join(out_dir, "storyboards", "shot1_20260904_203901.png"),
        "prompt": """Photorealistic 3D animation, 4 seconds.
A gentle calico cat Nini (white fur with orange and black patches, green eyes, white chest, short cute small cat proportions) wearing a brown leather apron stands behind a dark wooden barista counter inside a cozy warm cafe.
BACKGROUND: espresso machine on viewer's left background, dark wooden shelves on viewer's right background, hanging Edison bulb lights with soft golden bokeh.
Counter: Center has ONE empty white ceramic mug. Right counter has ONE small classic Bialetti Moka Express octagonal aluminum Moka pot (mustache man logo on front, black handle strictly on RIGHT side).
The cat holds ONE light grey POS card reader with glowing green screen up with its right paw on viewer's LEFT toward camera.
A credit card taps the device. Green confirmation light flashes.
ONLY AFTER green light: cat nods gently and places POS machine on far left of counter.
Cinematic warm golden cafe lighting, 8K fur texture.""",
    },
    {
        "output_name": "shot2.mp4",
        "image_path": os.path.join(out_dir, "storyboards", "shot2_20260904_205549.png"),
        "prompt": """Photorealistic 3D animation, 4 seconds. Continuation from Shot 1.
SAME calico cat Nini (white/orange/black patches, green eyes, short cute small cat proportions) WEARING THE EXACT SAME BROWN LEATHER APRON behind dark wooden counter.
BACKGROUND: same warm cafe interior — espresso machine on viewer's left, dark wooden shelves on viewer's right, golden bokeh.
Counter: Light grey POS machine rests ALONE on far-left corner (no paws touching). ONE white ceramic mug STATIONARY in center.
Cat uses its LEFT PAW (on viewer's right) to hold the Bialetti Moka pot by its RIGHT-SIDE black plastic handle, tilting the spout from the right to pour dark espresso into the center mug.
Moka pot has iconic Bialetti mustache man logo printed on front.
Cinematic warm golden cafe lighting, 8K fur detail.""",
    },
    {
        "output_name": "shot3.mp4",
        "image_path": os.path.join(out_dir, "storyboards", "shot3_20260904_203151.png"),
        "prompt": """Photorealistic 3D animation, 4 seconds. Continuation from Shot 2.
Close-up shot of SAME calico cat Nini (white/orange/black fur patches, green eyes, white chest, adorable small cat proportions) WEARING THE EXACT SAME BROWN LEATHER APRON.
BACKGROUND: same warm blurred cafe interior with golden bokeh lights.
On dark wooden counter on viewer's right: Bialetti Moka pot with black handle on right and mascot logo on front.
The cat lifts the SAME white ceramic mug (perfect heart latte art on top) with BOTH PAWS to offer it to the viewer.
Expression: A sweet, warm, polite, professional barista smile with twinkling green eyes, looking directly at the viewer with customer-service warmth. No tongue sticking out.
Cat softly extends the mug toward the viewer with both paws.
Soft warm golden cinematic lighting, 8K calico fur texture.""",
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
