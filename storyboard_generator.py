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
- EXACT BACKGROUND LAYOUT (100% IDENTICAL IN ALL SHOTS):
  - Viewer's LEFT background: Professional stainless steel espresso machine.
  - Viewer's RIGHT background: Dark wooden shelves with coffee bean bags and glass jars, hanging amber Edison bulb lights with soft golden bokeh.
  - Ambient moka_cat_12s warm golden lighting.
- EXACT COUNTERTOP OBJECT PLACEMENT (VIEWER'S PERSPECTIVE):
  - Far LEFT counter: POS Machine location (held up in cat's right paw on viewer's left in Shot 1; set down resting on far-left counter corner in Shot 2 and Shot 3).
  - CENTER counter: ONE white ceramic mug.
  - Far RIGHT counter: Bialetti Moka Express pot (black handle strictly on RIGHT side, mustache man logo on front).
- CAT-TO-MOKA-POT SCALE RATIO: Cat Nini is taller/larger than Moka pot in all shots (Moka pot reaches lower chest level only). Cat height and head size remain 100% IDENTICAL across all frames.
- CAT APPEARANCE & CLOTHING: Exactly match Reference Image 1 (Nini the calico cat) wearing the EXACT SAME brown leather apron with neck strap and front pocket in ALL shots.
- POS MACHINE APPEARANCE: Light grey front casing, glowing green screen at top, 3x4 numeric button grid layout. EXACT SAME in Shot 1, Shot 2, and Shot 3.
- ONE white ceramic mug. NEVER changes shape, size, or style.
- All objects obey gravity. Nothing floats.
=== END CONSTRAINTS ===
"""

# 分鏡清單：每一段是一個 dict
SHOTS = [
    {
        "id": "shot1",
        "title": "Shot 1（0–4s）：索卡付款",
        "description": "矮矮嬌小的妮妮穿棕圍裙，右爪持 POS 機（畫面左側）遞向鏡頭，綠燈確認後準備製作咖啡",
        "prompt": """Photorealistic 3D rendered storyboard frame. A gentle calico cat named Nini
(white fur with orange and black patches, green eyes, white chest, short compact body height and torso)
wearing a brown leather apron, standing behind a dark warm wooden barista counter inside a cozy ambient cafe.
BACKGROUND LAYOUT (STRICT): Professional stainless steel espresso machine on viewer's LEFT background; dark wooden shelves with coffee bags and glass jars on viewer's RIGHT background; hanging amber Edison bulb lights with golden bokeh.
COUNTERTOP LAYOUT: Center has ONE empty white ceramic mug. Far RIGHT counter has ONE small classic Bialetti Moka Express octagonal aluminum Moka pot (mustache man logo on front, black handle strictly on RIGHT side).
POS MACHINE: The cat holds ONE light grey POS card reader with glowing green screen up with its right paw on viewer's LEFT toward the camera.
Green confirmation light glows on POS screen.
Cinematic warm golden cafe lighting, 8K fur texture.""",
    },
    {
        "id": "shot2",
        "title": "Shot 2（4–8s）：倒咖啡 + 奶泡拉花",
        "description": "妮妮穿棕圍裙，左側吧台靜置同一台 POS 機，用左爪（畫面右側那隻手）抓握摩卡壺右側把手，傾斜倒咖啡入中央白瓷杯，Logo清晰可見",
        "prompt": """Photorealistic 3D rendered storyboard frame. Continuation from Shot 1.
SAME calico cat Nini (white fur with orange and black patches, green eyes, white chest, EXACT SAME short compact body height and short torso as Shot 1)
WEARING THE EXACT SAME BROWN LEATHER APRON WITH NECK STRAP AND FRONT POCKET.
BACKGROUND LAYOUT (EXACT SAME AS SHOT 1): Professional stainless steel espresso machine on viewer's LEFT background; dark wooden shelves with coffee bags on viewer's RIGHT background; hanging amber Edison lights with golden bokeh.
COUNTERTOP LAYOUT (EXACT SAME AS SHOT 1):
- Far LEFT counter: The EXACT SAME light grey POS card reader with glowing green screen rests ALONE on the far-left counter corner (no cat paws touching it).
- CENTER counter: ONE white ceramic mug stationary in center receiving dark espresso.
- Far RIGHT: Cat uses its LEFT PAW (the paw on viewer's RIGHT side) to hold the Bialetti Moka pot by its RIGHT-SIDE black plastic handle, tilting the spout towards the center mug.
- MOKA POT DETAILS: The iconic Bialetti mustache-man mascot logo ('L'omino con i baffi') and BIALETTI text MUST be clearly printed and visible on the front octagonal chamber wall of the Moka pot. Black handle remains strictly on the RIGHT side.
Cinematic warm golden cafe lighting, 8K calico fur detail.""",
    },
    {
        "id": "shot3",
        "title": "Shot 3（8–12s）：親切職業笑容遞咖啡",
        "description": "妮妮穿棕圍裙，左側吧台靜置同一台 POS 機，右側靜置摩卡壺，雙爪捧拉花咖啡露出親切甜美職業笑容",
        "prompt": """Photorealistic 3D rendered storyboard frame. Close-up shot inside cozy ambient cafe.
SAME calico cat Nini (white fur with orange and black patches, green eyes, white chest, EXACT SAME short cat body height and head size as Shot 1 and Shot 2)
WEARING THE EXACT SAME BROWN LEATHER APRON.
BACKGROUND LAYOUT (EXACT SAME AS SHOT 1 & 2): Professional stainless steel espresso machine on viewer's LEFT background; dark wooden shelves on viewer's RIGHT background; hanging amber Edison lights with golden bokeh.
COUNTERTOP LAYOUT (EXACT SAME AS SHOT 1 & 2):
- Far LEFT counter: The EXACT SAME light grey POS machine rests on the far-left counter corner.
- CENTER counter: Cat holds ONE white ceramic mug with heart latte art with BOTH PAWS.
- Far RIGHT counter: The EXACT SAME small Bialetti Moka Express Moka pot sits on counter (black handle strictly on RIGHT side, logo on front).
Expression: A sweet, warm, polite, professional barista smile with twinkling green eyes, looking directly at the viewer with customer-service warmth. No tongue out.
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


def generate_storyboard_image(shot: dict, client) -> str:
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
    print(f"\n[START] [{PROJECT_NAME}] 分鏡圖生成開始\n")
    client = genai.Client(api_key=API_KEY)
    image_paths = []
    for shot in SHOTS:
        path = generate_storyboard_image(shot, client)
        image_paths.append(path)

    print("\n[HTML] 生成 HTML 預覽頁面 ...")
    html_path = generate_html_preview(SHOTS, image_paths)
    print(f"[OK] 預覽頁面：{html_path}")
    print("\n[DONE] 完成！請用瀏覽器開啟預覽頁面確認分鏡，滿意後再提交影片生成任務。\n")


if __name__ == "__main__":
    main()
