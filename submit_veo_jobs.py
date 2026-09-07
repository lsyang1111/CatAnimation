"""
submit_veo_jobs.py
==================
Submits 4 Veo video generation jobs and saves operation names to ops.txt
"""
import os, sys

API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    print("ERROR: GEMINI_API_KEY not set", flush=True)
    sys.exit(1)

from google import genai
from google.genai import types

client = genai.Client(api_key=API_KEY)
out_dir = os.path.dirname(os.path.abspath(__file__))

SHOT_CONFIGS = [
    {
        "output_name": "shot1.mp4",
        "image_path": os.path.join(out_dir, "storyboards", "shot1_20260907_015223.png"),
        "prompt": """Photorealistic 3D animation, 4 seconds. Cozy warm cafe interior.
The cat barista holds a POS card reader toward the camera with its right paw.
A credit card taps the device. The green screen light flashes with confirmation.
The cat nods gently with a professional friendly smile, then slowly places the POS machine down on the far-left corner of the counter.
All props (POS machine, Moka pot, mug) keep identical color, angle, shape, and height — no scale drift.
Every prop rests fully on the counter surface — real gravity, no floating or hovering, no gaps.
Smooth subtle cinematic camera motion. Warm golden ambient cafe lighting.""",
    },
    {
        "output_name": "shot2.mp4",
        "image_path": os.path.join(out_dir, "storyboards", "shot2_20260907_015237.png"),
        "prompt": """Photorealistic 3D animation, 4 seconds. Continuation from Shot 1.
The cat barista tilts the Moka pot to pour dark espresso into the white ceramic mug.
While pouring, the cat's eyes drift sideways toward the small milk jug on the counter with a longing, tempted expression.
The cat's cheeks flush slightly with inner conflict between duty and desire.
All props (POS machine, Moka pot, mug, milk jug) keep identical color, angle, shape, and height as Shot 1 — no scale drift.
Every prop rests fully on the counter surface — real gravity, no floating or hovering, no gaps.
Smooth subtle cinematic motion. Warm golden cafe lighting.""",
    },
    {
        "output_name": "shot3.mp4",
        "image_path": os.path.join(out_dir, "storyboards", "shot3_20260907_015246.png"),
        "prompt": """Photorealistic 3D animation, 4 seconds. Continuation from Shot 2.
The cat calmly and naturally leans down and takes a relaxed sip of milk straight from the jug, as an easy, unhurried little break — not sneaky or secretive.
Eyes close gently in simple contentment. A tiny drop of white milk appears on the pink nose and the corner of the mouth.
Posture stays relaxed and open, with a soft natural smile — no tension, no guilt.
All props (POS machine, Moka pot, mug, milk jug) keep identical color, angle, shape, and height as previous shots — no scale drift.
Every prop rests fully on the counter surface — real gravity, no floating or hovering, no gaps.
Smooth cinematic motion. Warm golden cafe lighting.""",
    },
    {
        "output_name": "shot4.mp4",
        "image_path": os.path.join(out_dir, "storyboards", "shot4_20260907_015256.png"),
        "prompt": """Photorealistic 3D animation, 4 seconds. Continuation from Shot 3. Final shot.
The cat gently straightens up, resumes professional posture, eyes open wide with a warm sweet smile.
The cat lifts the white ceramic mug with heart latte art with both paws and gently extends it toward the viewer.
Eyes twinkle with cheerful, genuine warmth — relaxed and happy, no guilt.
All props (POS machine, Moka pot, mug) keep identical color, angle, shape, and height as previous shots — no scale drift.
Every prop rests fully on the counter surface — real gravity, no floating or hovering, no gaps.
Smooth gentle cinematic motion. Warm golden cafe lighting.""",
    },
]

ops_file = os.path.join(out_dir, "veo_ops.txt")
print("Submitting 4 Veo jobs...", flush=True)

with open(ops_file, "w") as f:
    for shot in SHOT_CONFIGS:
        name = shot["output_name"]
        img_path = shot["image_path"]
        print(f"  Submitting {name}...", flush=True)
        with open(img_path, "rb") as img_f:
            img_bytes = img_f.read()
        ext = os.path.splitext(img_path)[1].lower()
        mime = "image/jpeg" if ext in (".jpg", ".jpeg") else "image/png"
        op = client.models.generate_videos(
            model="veo-3.1-fast-generate-preview",
            prompt=shot["prompt"],
            image=types.Image(
                image_bytes=img_bytes,
                mime_type=mime,
            ),
        )
        line = f"{name}|{op.name}"
        f.write(line + "\n")
        f.flush()
        print(f"  [SUBMITTED] {name} -> {op.name}", flush=True)

print(f"\nAll 4 jobs submitted! Operation names saved to: {ops_file}", flush=True)
print("Now run: python poll_veo_jobs.py", flush=True)
