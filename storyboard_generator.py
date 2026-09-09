"""
storyboard_generator.py
=======================
Standard storyboard image generator.
Usage: Edit the SHOTS list below, then run this script.

pip install google-genai pillow
"""
import sys
import io
# Fix Windows console encoding
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

import os
import base64
import json
from datetime import datetime
from google import genai
from google.genai import types

# ============================================================
# ✏️  在這裡填入你的分鏡資料
# ============================================================

PROJECT_NAME = "三花貓妮妮咖啡廳系列"

# 參考照片路徑（設定後 AI 會以這些照片作為角色與道具外觀基準）
NINI_REF_PATH = r"C:\Users\lsyan\Documents\Code\CatAnimation\nini_reference.jpg"
MOKA_REF_PATH = r"C:\Users\lsyan\Documents\Code\CatAnimation\moka_reference.png"
POS_REF_PATH = r"C:\Users\lsyan\Documents\Code\CatAnimation\pos_reference.png"

# 全局硬性規則（會自動加到每段 prompt 前面）
GLOBAL_CONSTRAINTS = """
=== HARD CONSTRAINTS (NEVER VIOLATE) ===
- LOCKED CAMERA PERSPECTIVE & LENS (100% IDENTICAL CAMERA RIG IN ALL SHOTS):
  - Fixed Tripod Camera Angle: Eye-level perspective directly facing Nini across the barista counter (customer viewpoint).
  - Fixed Lens: 50mm cinematic prime lens, f/2.8 aperture, zero lens distortion.
  - Fixed Framing: Medium Shot (chest-up view of Nini, showing the full countertop width from far-left POS machine to far-right Moka pot).
  - Fixed Horizon: The wooden countertop surface level must remain at the exact same vertical height in all 4 frames.
- LOCKED PROP ORIENTATION & ROTATIONAL ANGLES (100% IDENTICAL IN ALL SHOTS):
  - POS MACHINE ANGLES: Light grey casing with glowing green screen.
    * In Shot 1: Held up in cat's right paw, facing straight forward toward camera (0-degree rotation).
    * In Shot 2, Shot 3, Shot 4: Placed resting upright on far-left counter corner, facing STRAIGHT FORWARD toward camera (0-degree rotation, screen and 3x4 buttons facing viewer directly). NEVER rotated sideways or tilted at odd angles.
  - MOKA POT ANGLES: Classic octagonal Bialetti Moka pot.
    * Front face with mustache man logo faces STRAIGHT FORWARD toward camera in all shots.
    * Black plastic handle points STRICTLY 90 DEGREES TO THE RIGHT side in all shots.
- EXACT CAT FACIAL & FUR MARKINGS (100% IDENTICAL IN ALL SHOTS): Exactly match Reference Image 1 (Nini the calico cat). The head/forehead has light orange/ginger tabby fur patches with small tiger stripes, white snout/lower face, pink nose, and white chest. NO heavy solid black patches on forehead or ears. MUST match Shot 1 and Shot 3 fur coloring.
- EXACT BACKGROUND LAYOUT (100% IDENTICAL IN ALL SHOTS):
  - Viewer's LEFT background: Professional stainless steel espresso machine.
  - Viewer's RIGHT background: Dark wooden shelves with coffee bean bags and glass jars, hanging amber Edison bulb lights with soft golden bokeh.
  - Ambient warm golden lighting.
- EXACT COUNTERTOP OBJECT PLACEMENT (VIEWER'S PERSPECTIVE):
  - Far LEFT counter: POS Machine location (held up in cat's right paw on viewer's left in Shot 1; set down resting on far-left counter corner facing camera in Shot 2, Shot 3, and Shot 4).
  - CENTER counter: ONE white ceramic mug.
  - Far RIGHT counter: Bialetti Moka Express pot (black handle strictly on RIGHT side, mustache man logo on front).
- CAT-TO-MOKA-POT SCALE RATIO: Cat Nini is taller/larger than Moka pot in all shots (Moka pot reaches lower chest level only). Cat height and head size remain 100% IDENTICAL across all frames.
- CAT APPEARANCE & CLOTHING: Exactly match Reference Image 1 (Nini the calico cat) wearing the EXACT SAME brown leather apron with neck strap and front pocket in ALL shots.
- ONE white ceramic mug. NEVER changes shape, size, or style.
- All objects obey gravity. Nothing floats.
=== END CONSTRAINTS ===
"""

# 分鏡清單：每一段是一個 dict
SHOTS = [
    {
        "id": "shot1",
        "title": "Shot 1（0–4s）：刷卡付款",
        "description": "矮矮嬌小的妮妮穿棕圍裙，右爪持 POS 機（畫面左側）遞向鏡頭，綠燈確認後準備製作咖啡",
        "prompt": """Photorealistic 3D rendered storyboard frame. Fixed 50mm medium shot over barista counter.
A gentle calico cat named Nini (white fur with orange/ginger tabby head patches, green eyes, white chest, pink nose, short compact body height and torso)
wearing a brown leather apron, standing behind a dark warm wooden barista counter inside a cozy ambient cafe.
CAMERA & ANGLE: Eye-level tripod medium shot, perfectly straight facing the cat over the counter.
BACKGROUND LAYOUT (STRICT): Professional stainless steel espresso machine on viewer's LEFT background; dark wooden shelves with coffee bags and glass jars on viewer's RIGHT background; hanging amber Edison bulb lights with golden bokeh.
COUNTERTOP LAYOUT: Center has ONE empty white ceramic mug. Far RIGHT counter has ONE small classic Bialetti Moka Express octagonal aluminum Moka pot (mustache man logo on front, black handle strictly on RIGHT side).
POS MACHINE: The cat holds ONE light grey POS card reader with glowing green screen up with its right paw on viewer's LEFT toward the camera.
Green confirmation light glows on POS screen. Cat expression is professional and friendly.
Cinematic warm golden cafe lighting, 8K fur texture.""",
    },
    {
        "id": "shot2",
        "title": "Shot 2（4–8s）：倒咖啡，眼神飄向牛奶",
        "description": "妮妮穿棕圍裙，左爪握摩卡壺把手倒咖啡，但眼神悄悄飄向旁邊的牛奶罐，露出渴望的神情",
        "prompt": """Photorealistic 3D rendered storyboard frame. Continuation from Shot 1. Fixed 50mm medium shot over barista counter (EXACT SAME CAMERA ANGLE AND DISTANCE AS SHOT 1).
The cat's forehead is entirely light orange/ginger tabby fur with small tiger stripes. White snout, pink nose, white chest, green eyes. WEARING THE EXACT SAME BROWN LEATHER APRON WITH NECK STRAP AND FRONT POCKET.
CAMERA & ANGLE: Eye-level tripod medium shot, perfectly straight facing the cat over the counter.
BACKGROUND LAYOUT (EXACT SAME AS SHOT 1): Professional stainless steel espresso machine on viewer's LEFT background; dark wooden shelves with coffee bags on viewer's RIGHT background; hanging amber Edison lights with golden bokeh.
COUNTERTOP LAYOUT (EXACT SAME AS SHOT 1):
- Far LEFT counter: The EXACT SAME light grey POS card reader with glowing green screen rests ALONE on the far-left counter corner. The POS machine is resting untouched, upright on the counter.
- CENTER counter: ONE white ceramic mug stationary in center receiving dark espresso from the Moka pot spout.
- Next to the mug: ONE small white milk jug or glass of fresh white milk sits on the counter.
- Far RIGHT: Cat uses its LEFT PAW (the paw on viewer's RIGHT side) to hold the Bialetti Moka pot by its RIGHT-SIDE black plastic handle, tilting the spout towards the center mug.
- MOKA POT DETAILS: The iconic Bialetti mustache-man mascot logo and BIALETTI text clearly visible on the front. Black handle remains strictly on the RIGHT side.
EXPRESSION: The cat's eyes drift sideways toward the milk jug with a longing, tempted expression — a gentle internal struggle between duty and desire. Slight cheek flush of temptation.
Cinematic warm golden cafe lighting, 8K calico fur detail.""",
    },
    {
        "id": "shot3",
        "title": "Shot 3（8–12s）：自然品嚐鮮奶",
        "description": "妮妮低頭自然輕鬆地喝一口鮮奶，眼睛微閉享受香醇奶香，神情十分放鬆自在與滿足",
        "prompt": """Photorealistic 3D rendered storyboard frame. Continuation from Shot 2. Fixed 50mm medium shot over barista counter (EXACT SAME CAMERA ANGLE AND DISTANCE AS SHOT 1 & 2).
The cat's forehead is entirely light orange/ginger tabby fur. White snout, pink nose, white chest, green eyes. WEARING THE EXACT SAME BROWN LEATHER APRON.
CAMERA & ANGLE: Eye-level tripod medium shot, perfectly straight facing the cat over the counter.
BACKGROUND LAYOUT (EXACT SAME AS SHOT 1 & 2): Professional stainless steel espresso machine on viewer's LEFT background; dark wooden shelves on viewer's RIGHT background; hanging amber Edison lights with golden bokeh.
COUNTERTOP LAYOUT:
- Far LEFT counter: The EXACT SAME light grey POS machine rests on the far-left counter corner. The POS machine is resting untouched, upright on the counter.
- CENTER counter: The white ceramic mug and small white milk jug are on the counter.
- Far RIGHT counter: The EXACT SAME small Bialetti Moka pot sits on counter (black handle strictly on RIGHT side, logo on front).
ACTION: Nini naturally takes a peaceful, gentle sip from the milk jug. She leans slightly forward with her eyes closed in pure relaxation and enjoyment, tasting the rich fresh milk. Her expression is calm, sweet, and content — completely natural, happy, and relaxed with no guilt or hesitation. A tiny drop of white milk rests gently on her pink nose.
Soft warm golden cinematic lighting, 8K calico fur detail.""",
    },
    {
        "id": "shot4",
        "title": "Shot 4（12–16s）：假裝沒事，捧咖啡遞給客人",
        "description": "妮妮迅速恢復職業笑容，嘴角還帶著一點點奶漬，雙爪捧著拉花咖啡遞向鏡頭，帶著甜蜜又有點心虛的笑容",
        "prompt": """Photorealistic 3D rendered storyboard frame. Final shot. Fixed 50mm medium shot over barista counter (EXACT SAME CAMERA ANGLE AND DISTANCE AS SHOT 1, 2 & 3).
The cat's forehead is entirely light orange/ginger tabby fur. White snout, pink nose, white chest, bright green eyes. WEARING THE EXACT SAME BROWN LEATHER APRON.
CAMERA & ANGLE: Eye-level tripod medium shot, perfectly straight facing the cat over the counter.
BACKGROUND LAYOUT (EXACT SAME AS ALL PREVIOUS SHOTS): Professional stainless steel espresso machine on viewer's LEFT background; dark wooden shelves on viewer's RIGHT background; hanging amber Edison lights with golden bokeh.
COUNTERTOP LAYOUT:
- Far LEFT counter: The EXACT SAME light grey POS machine rests on the far-left counter corner. The POS machine is resting untouched, upright on the counter.
- CENTER counter: Cat holds ONE white ceramic mug with a beautiful heart latte art on top with BOTH PAWS, extending it warmly toward the viewer.
- Far RIGHT counter: The EXACT SAME small Bialetti Moka pot sits on counter (black handle strictly on RIGHT side, logo on front).
EXPRESSION: A sweet, warm, professional barista smile — but with a tiny hint of guilt and mischief in the eyes, as if she is hoping the customer did not notice she sipped the milk. A nearly invisible tiny white milk residue trace remains at the very corner of her lip. Eyes are twinkling with a cheerful, slightly sheepish warmth.
Soft warm golden cinematic lighting, 8K calico fur texture.""",
    },
]


# ============================================================
# 🔧  以下為執行邏輯，通常不需要修改
# ============================================================

API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("請設定環境變數 GEMINI_API_KEY，例如：$env:GEMINI_API_KEY='你的API金鑰'")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "storyboards")


def generate_storyboard_image(shot: dict, client, master_ref_path: str = None) -> str:
    """Generate a storyboard image for a single shot. Returns saved file path."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    full_prompt = GLOBAL_CONSTRAINTS.strip() + "\n\n" + shot["prompt"].strip()

    print(f"  Generating {shot['id']}: {shot['title']} ...")

    # Build contents: include both reference images if provided
    contents_parts = []
    
    if NINI_REF_PATH and os.path.exists(NINI_REF_PATH):
        with open(NINI_REF_PATH, "rb") as f:
            nini_bytes = f.read()
        ext = os.path.splitext(NINI_REF_PATH)[1].lower()
        mime = "image/jpeg" if ext in (".jpg", ".jpeg") else "image/png"
        contents_parts.append(types.Part(text="REFERENCE IMAGE 1: Cat Protagonist Nini (preserve exact fur, facial markings, and eyes):"))
        contents_parts.append(types.Part(inline_data=types.Blob(mime_type=mime, data=nini_bytes)))
        print(f"  [REF] Using Nini photo: {os.path.basename(NINI_REF_PATH)}")

    if MOKA_REF_PATH and os.path.exists(MOKA_REF_PATH):
        with open(MOKA_REF_PATH, "rb") as f:
            moka_bytes = f.read()
        ext = os.path.splitext(MOKA_REF_PATH)[1].lower()
        mime = "image/jpeg" if ext in (".jpg", ".jpeg") else "image/png"
        contents_parts.append(types.Part(text="REFERENCE IMAGE 2: Bialetti Moka Express Pot (MUST copy this EXACT mustache-man line art logo and BIALETTI text onto the upper chamber face of the Moka pot):"))
        contents_parts.append(types.Part(inline_data=types.Blob(mime_type=mime, data=moka_bytes)))
        print(f"  [REF] Using Moka pot photo: {os.path.basename(MOKA_REF_PATH)}")

    if POS_REF_PATH and os.path.exists(POS_REF_PATH):
        with open(POS_REF_PATH, "rb") as f:
            pos_bytes = f.read()
        ext = os.path.splitext(POS_REF_PATH)[1].lower()
        mime = "image/jpeg" if ext in (".jpg", ".jpeg") else "image/png"
        contents_parts.append(types.Part(text="REFERENCE IMAGE 3: POS Payment Terminal (MUST replicate this EXACT light-grey body, glowing green screen, 3x4 button layout with red/green bottom buttons):"))
        contents_parts.append(types.Part(inline_data=types.Blob(mime_type=mime, data=pos_bytes)))
        print(f"  [REF] Using POS photo: {os.path.basename(POS_REF_PATH)}")

    if master_ref_path and os.path.exists(master_ref_path):
        with open(master_ref_path, "rb") as f:
            master_bytes = f.read()
        ext = os.path.splitext(master_ref_path)[1].lower()
        mime = "image/jpeg" if ext in (".jpg", ".jpeg") else "image/png"
        contents_parts.append(types.Part(text="REFERENCE IMAGE 4: MASTER BASELINE ANCHOR FRAME (SHOT 1) — MUST COPY EXACT BARISTA COUNTER HEIGHT, BACKGROUND DEPTH, LIGHTING, CAT SCALE, FUR COLOR, APRON, AND PROPS FROM THIS FRAME:"))
        contents_parts.append(types.Part(inline_data=types.Blob(mime_type=mime, data=master_bytes)))
        print(f"  [REF] Using Master Anchor Shot 1: {os.path.basename(master_ref_path)}")

    contents_parts.append(types.Part(text="SCENE PROMPT:\n" + full_prompt))
    contents = contents_parts

    response = client.models.generate_content(
        model="gemini-2.5-flash-image",
        contents=contents,
        config=types.GenerateContentConfig(
            response_modalities=["IMAGE", "TEXT"],
        ),
    )
    # Extract image bytes from response parts
    image_data = None
    for part in response.candidates[0].content.parts:
        if part.inline_data is not None:
            image_data = part.inline_data.data
            break
    if image_data is None:
        raise ValueError(f"No image returned for {shot['id']}.")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{shot['id']}_{timestamp}.png"
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, "wb") as f:
        f.write(base64.b64decode(image_data) if isinstance(image_data, str) else image_data)
    print(f"  [OK] Saved: {filepath}")
    return filepath


def generate_html_preview(shots: list, image_paths: list) -> str:
    """Generate an HTML storyboard preview page."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    cards_html = ""
    for shot, img_path in zip(shots, image_paths):
        abs_path = os.path.abspath(img_path).replace("\\", "/")
        cards_html += f"""
        <div class="card">
            <div class="card-header">
                <span class="shot-id">{shot['id'].upper()}</span>
                <h2>{shot['title']}</h2>
            </div>
            <img src="file:///{abs_path}" alt="{shot['title']}">
            <div class="card-body">
                <p class="description">{shot['description']}</p>
                <details>
                    <summary>查看完整 Prompt</summary>
                    <pre>{shot['prompt'].strip()}</pre>
                </details>
                <div class="checklist">
                    <strong>確認清單：</strong>
                    <label><input type="checkbox"> 視覺風格符合預期</label>
                    <label><input type="checkbox"> 道具位置正確</label>
                    <label><input type="checkbox"> 貓咪外觀OK</label>
                </div>
            </div>
        </div>"""

    html = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<title>{PROJECT_NAME} — 分鏡確認</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: 'Segoe UI', sans-serif; background: #0f0f0f; color: #eee; padding: 2rem; }}
  h1 {{ text-align: center; font-size: 1.8rem; margin-bottom: 0.5rem; color: #fff; }}
  .meta {{ text-align: center; color: #888; margin-bottom: 2rem; font-size: 0.9rem; }}
  .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(360px, 1fr)); gap: 1.5rem; }}
  .card {{ background: #1a1a1a; border-radius: 12px; overflow: hidden; border: 1px solid #333; }}
  .card-header {{ padding: 1rem 1.2rem 0.5rem; display: flex; align-items: center; gap: 0.8rem; }}
  .shot-id {{ background: #7c3aed; color: white; border-radius: 6px; padding: 2px 10px;
              font-size: 0.75rem; font-weight: bold; letter-spacing: 1px; }}
  h2 {{ font-size: 1rem; color: #ddd; }}
  img {{ width: 100%; display: block; }}
  .card-body {{ padding: 1rem 1.2rem 1.2rem; }}
  .description {{ color: #aaa; font-size: 0.9rem; margin-bottom: 0.8rem; line-height: 1.6; }}
  details {{ margin-bottom: 0.8rem; }}
  summary {{ cursor: pointer; color: #7c3aed; font-size: 0.85rem; margin-bottom: 0.4rem; }}
  pre {{ background: #111; border-radius: 6px; padding: 0.8rem; font-size: 0.75rem;
         color: #9ca3af; white-space: pre-wrap; word-break: break-word; }}
  .checklist {{ display: flex; flex-direction: column; gap: 0.4rem; }}
  .checklist strong {{ color: #ccc; font-size: 0.85rem; margin-bottom: 0.2rem; display: block; }}
  label {{ display: flex; align-items: center; gap: 0.5rem; color: #aaa; font-size: 0.85rem;
           cursor: pointer; }}
  input[type=checkbox] {{ accent-color: #7c3aed; width: 14px; height: 14px; }}
</style>
</head>
<body>
<h1>🎬 {PROJECT_NAME}</h1>
<p class="meta">分鏡確認頁面 · 生成時間：{timestamp} · 共 {len(shots)} 段分鏡</p>
<div class="grid">{cards_html}</div>
</body>
</html>"""
    html_path = os.path.join(OUTPUT_DIR, "storyboard_preview.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    return html_path


def main():
    print(f"\n[START] [{PROJECT_NAME}] 分鏡圖生成開始（使用主影格鏈接 Pipeline）\n")
    client = genai.Client(api_key=API_KEY)
    image_paths = []
    master_shot1_path = None

    for shot in SHOTS:
        path = generate_storyboard_image(shot, client, master_ref_path=master_shot1_path)
        if shot["id"] == "shot1" and os.path.exists(path):
            master_shot1_path = path
            print(f"  [MASTER ANCHOR LOCKED] Shot 1 reference frame set to: {os.path.basename(path)}")
        image_paths.append(path)

    print("\n[HTML] 生成 HTML 預覽頁面 ...")
    html_path = generate_html_preview(SHOTS, image_paths)
    print(f"[OK] 預覽頁面：{html_path}")
    print("\n[DONE] 完成！請確認三張分鏡圖。\n")


if __name__ == "__main__":
    main()

