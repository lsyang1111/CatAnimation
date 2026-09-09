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
        "image_path": os.path.join(out_dir, "storyboards", "shot1_20260909_220434.png"),
        "prompt": """Photorealistic 3D animation, 4 seconds. Fixed 50mm eye-level medium camera shot over counter.
SEQUENCE:
1. (0.0s) The cat barista holds the POS card reader facing straight forward toward the camera with its right paw. She waits calmly and patiently.
2. (0.8s) A customer's credit card gently taps the POS screen. The cat holds completely still — a brief 1-second pause while the payment processes.
3. (2.0s) The POS screen suddenly lights up with a vivid, bright GLOWING GREEN light — the payment is confirmed. The green light radiates warmth.
4. (2.8s) The cat gives a warm, professional nod and a gentle smile upon seeing the green confirmation.
5. (3.4s) The cat slowly and smoothly places the POS machine down on the far-left corner of the counter, set upright facing straight forward toward the camera.
Fixed camera, zero lens distortion. Warm golden ambient cafe lighting.""",
    },
    {
        "output_name": "shot2.mp4",
        "image_path": os.path.join(out_dir, "storyboards", "shot2_20260904_215331.png"),
        "prompt": """Photorealistic 3D animation, 4 seconds. Continuation from Shot 1. Fixed 50mm eye-level medium camera shot over counter (EXACT SAME CAMERA RIG).
The light grey POS card reader rests untouched on far-left counter corner facing straight forward toward the camera.
The cat barista tilts the Moka pot to pour dark espresso into the white ceramic mug.
While pouring, the cat's eyes drift sideways toward the small milk jug on the counter with a longing, tempted expression.
The cat's cheeks flush slightly with inner conflict between duty and desire.
Smooth subtle cinematic motion, zero lens distortion. Warm golden cafe lighting.""",
    },
    {
        "output_name": "shot3.mp4",
        "image_path": os.path.join(out_dir, "storyboards", "shot3_20260904_215351.png"),
        "prompt": """Photorealistic 3D animation, 4 seconds. Continuation from Shot 2. Fixed 50mm eye-level medium camera shot over counter (EXACT SAME CAMERA RIG).
The light grey POS card reader rests untouched on far-left counter corner facing straight forward toward the camera.
The cat leans forward and naturally takes a gentle, peaceful sip from the milk jug.
Eyes close slowly in pure bliss and relaxation, enjoying the rich fresh milk.
A tiny drop of white milk appears on the pink nose and corner of the mouth.
The cat's expression is calm, sweet, and completely content — relaxed and natural with no guilt.
Smooth cinematic motion, zero lens distortion. Warm golden cafe lighting.""",
    },
    {
        "output_name": "shot4.mp4",
        "image_path": os.path.join(out_dir, "storyboards", "shot4_20260904_215409.png"),
        "prompt": """Photorealistic 3D animation, 4 seconds. Continuation from Shot 3. Final shot. Fixed 50mm eye-level medium camera shot over counter (EXACT SAME CAMERA RIG).
The light grey POS card reader rests untouched on far-left counter corner facing straight forward toward the camera.
The cat quickly straightens up, resumes professional posture, eyes open wide with a warm sweet smile.
The cat lifts the white ceramic mug with heart latte art with both paws and gently extends it toward the viewer.
Eyes twinkle with cheerful, slightly sheepish warmth.
Smooth gentle cinematic motion, zero lens distortion. Warm golden cafe lighting.""",
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
