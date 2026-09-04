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
- CAT PROPORTIONS: Small compact cat body height, short cute paws, realistic small cat proportions (not tall humanoid). Wooden counter top reaches up to cat's chest/shoulder level so cat looks cute, small and short.
- CAT APPEARANCE: Exactly match Reference Image 1 (Nini the calico cat).
- MOKA POT APPEARANCE: Exactly match Reference Image 2 (Bialetti Moka Express pot). MUST copy the EXACT line-art logo of the little man with mustache raising one finger ('L'omino con i baffi') and the 'BIALETTI' text from Reference Image 2 onto the Moka pot's upper chamber.
- POS MACHINE APPEARANCE: Exactly match Reference Image 3 (Payment terminal). Light grey front casing, glowing green screen at top, 3x4 numeric button layout with red bottom-left button and green bottom-right button. EXACT SAME color, button layout, and shape in both Shot 1 and Shot 2.
- ONE white ceramic mug. NEVER changes shape, size, or style.
- Cat does NOT start coffee-making until AFTER green payment light confirms.
- All objects obey gravity. Nothing floats.
=== END CONSTRAINTS ===
"""

# 分鏡清單：每一段是一個 dict
SHOTS = [
    {
        "id": "shot1",
        "title": "Shot 1（0–4s）：索卡付款",
        "description": "矮矮可愛的妮妮右爪持 POS 機遞向鏡頭，顧客刷卡，綠燈確認後放下 POS 機開始製作咖啡",
        "prompt": """Photorealistic 3D rendered storyboard frame. A gentle calico cat named Nini
(white fur with orange and black patches, green eyes, white chest)
with a cute short body height and small compact cat proportions (counter top reaches up to its chest),
wearing a brown leather apron, standing behind a wooden barista counter inside a cozy cafe.
BACKGROUND: warm cafe interior with wooden shelves holding coffee bags and jars,
a professional espresso machine visible behind, hanging Edison bulb lights,
soft golden bokeh — the cat looks like a sweet part-time cafe worker.
Counter has ONLY TWO items: ONE empty white ceramic mug in center,
ONE classic Bialetti Moka Express octagonal aluminum Moka pot (silver-grey metallic vintage finish with iconic mustache man raising finger logo printed on front chamber wall, black handle on the RIGHT side).
There is NO POS machine on the counter table.
The cat holds ONE POS card reader up with its right paw toward the camera — the ONLY POS machine in scene.
Green confirmation light glows on the POS screen in the cat's paw.
Cinematic warm cafe lighting, 8K fur texture.""",
    },
    {
        "id": "shot2",
        "title": "Shot 2（4–8s）：倒咖啡 + 奶泡拉花",
        "description": "矮矮可愛的妮妮傾斜摩卡壺（造型不變）倒入同一個白瓷杯，接著用奶泡壺拉出愛心",
        "prompt": """Photorealistic 3D rendered storyboard frame. Continuation from Shot 1.
SAME calico cat Nini (white fur with orange and black patches, green eyes, white chest, short cute small cat proportions)
in brown leather apron behind a wooden barista counter inside a cozy cafe (counter height reaches cat's chest level).
BACKGROUND: same warm cafe interior — wooden shelves with coffee bags, espresso machine, Edison bulb lights, golden bokeh.
Counter: POS card machine placed on far LEFT corner (still visible), ONE white ceramic mug stationary in center
receiving dark espresso being poured.
Cat grips the EXACT SAME Bialetti Moka Express octagonal aluminum Moka pot (with iconic mustache man raising finger logo on front) by its RIGHT-SIDE black handle,
tilting it to pour (shape and logo unchanged, angle only). Warm steam rising from the mug.
Cinematic warm cafe lighting, 8K calico fur detail.""",
    },
    {
        "id": "shot3",
        "title": "Shot 3（8–12s）：偷舔奶泡 ➔ 楚楚可憐遞給你",
        "description": "矮矮嬌小的妮妮雙爪捧杯偷舔奶泡被抓包，露出最無辜楚楚可憐的表情，輕輕遞出咖啡",
        "prompt": """Photorealistic 3D rendered storyboard frame. Close-up shot inside a cozy cafe.
SAME calico cat Nini (white fur with orange and black patches, green eyes, white chest, adorable small cat proportions)
in brown leather apron.
BACKGROUND: warm blurred cafe interior with golden bokeh lights and wooden shelves.
On the wooden counter next to the cat: the EXACT SAME Bialetti Moka Express octagonal aluminum Moka pot with iconic mustache man raising finger logo on front.
Cat holds ONE white ceramic mug with heart-shaped latte art with BOTH PAWS —
caught licking milk foam with its small pink tongue.
Expression: NOT guilty smirk — the most innocent, soft, doe-eyed look.
Green eyes wide and glistening, slightly parted mouth, expression says 'I'm sorry... but it was so good'.
Cat softly extends the mug toward the camera/viewer with both paws.
Soft warm cinematic lighting, 8K calico fur texture, adorably innocent expression.""",
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
