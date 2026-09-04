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

PROJECT_NAME = "黑貓丞丞咖啡廳系列"

# 全局硬性規則（會自動加到每段 prompt 前面）
GLOBAL_CONSTRAINTS = """
=== HARD CONSTRAINTS (NEVER VIOLATE) ===
- ONE white ceramic mug. NEVER changes shape, size, or style.
- Octagonal metal Moka pot. Black handle on RIGHT SIDE ONLY. Shape never changes.
- Cat does NOT start coffee-making until AFTER green payment light confirms.
- All objects obey gravity. Nothing floats.
=== END CONSTRAINTS ===
"""

# 分鏡清單：每一段是一個 dict
SHOTS = [
    {
        "id": "shot1",
        "title": "Shot 1（0–4s）：索卡付款",
        "description": "丞丞右爪持 POS 機遞向鏡頭，顧客刷卡，綠燈確認後放下 POS 機開始製作咖啡",
        "prompt": """Photorealistic 3D rendered storyboard frame. Sleek black cat with emerald green eyes
and brown leather apron standing behind a wooden barista counter inside a cozy cafe.
BACKGROUND: warm cafe interior with wooden shelves holding coffee bags and jars, 
a professional espresso machine visible behind, hanging Edison bulb lights, 
soft golden bokeh — the cat looks like a part-time cafe worker.
Counter has ONLY TWO items: ONE empty white ceramic mug in center,
ONE classic dark aluminum octagonal Moka pot (Bialetti-style, matte dark body, black handle on the RIGHT side).
There is NO POS machine on the counter table.
The cat holds ONE POS card reader up with its right paw toward the camera — the ONLY POS machine in scene.
Green confirmation light glows on the POS screen in the cat's paw.
Cinematic warm cafe lighting, 8K black fur texture.""",
    },
    {
        "id": "shot2",
        "title": "Shot 2（4–8s）：倒咖啡 + 奶泡拉花",
        "description": "丞丞傾斜摩卡壺（造型不變）倒入同一個白瓷杯，接著用奶泡壺拉出愛心",
        "prompt": """Photorealistic 3D rendered storyboard frame. Continuation from Shot 1.
Sleek black cat with emerald green eyes and brown leather apron behind a wooden barista counter.
BACKGROUND: same warm cafe interior — wooden shelves with coffee bags, espresso machine, Edison bulb lights, golden bokeh.
Counter: POS card machine placed on far LEFT corner (still visible), ONE white ceramic mug stationary in center
receiving dark espresso being poured.
Cat grips the classic dark aluminum Bialetti-style octagonal Moka pot by its RIGHT-SIDE black handle,
tilting it to pour (shape unchanged, angle only). Warm steam rising from the mug.
Cinematic warm cafe lighting, 8K detail.""",
    },
    {
        "id": "shot3",
        "title": "Shot 3（8–12s）：偷舔奶泡 ➔ 害羞遞給你",
        "description": "丞丞雙爪捧起有愛心拉花的白瓷杯，偷舔奶泡被抓包，翡翠眼瞇成月牙害羞遞出",
        "prompt": """Photorealistic 3D rendered storyboard frame. Close-up shot inside a cozy cafe.
Sleek black cat with emerald green eyes and brown leather apron.
BACKGROUND: warm blurred cafe interior with golden bokeh lights and wooden shelves — part-time barista vibe.
Cat holds ONE white ceramic mug with heart-shaped latte art with BOTH PAWS —
caught in the act of licking milk foam with its small pink tongue.
The cat's emerald eyes squint into happy crescent moon shapes, bashful and charming guilty expression.
Cat gently extends the mug toward the camera/viewer.
Soft warm cinematic lighting, 8K black fur texture, adorable guilty expression.""",
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
    response = client.models.generate_content(
        model="gemini-2.5-flash-image",
        contents=full_prompt,
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
        raise ValueError(f"No image returned for {shot['id']}. Response: {response.text}")

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
