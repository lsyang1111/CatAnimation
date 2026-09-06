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
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
NINI_REF_PATH = os.path.join(_SCRIPT_DIR, "nini_reference.jpg")
MOKA_REF_PATH = os.path.join(_SCRIPT_DIR, "moka_reference.png")
POS_REF_PATH = os.path.join(_SCRIPT_DIR, "pos_reference.png")

# 全局硬性規則（會自動加到每段 prompt 前面）
GLOBAL_CONSTRAINTS = """
=== HARD CONSTRAINTS (NEVER VIOLATE) ===
- NINI'S ROLE (CRITICAL CONTEXT): Nini is a PART-TIME CAFE EMPLOYEE (咖啡廳打工仔) — a working barista/staff member, NOT a customer. She stands on the STAFF side of the counter, wears a work apron and a round employee ID tag on a cord around her neck. Every shot must read as "an employee at work," never as a patron. IMPORTANT: at any given moment she only handles ONE task/prop at a time (per that shot's own instructions below) — never show her holding more than what that specific shot describes.
- EXACT CAT FACIAL & FUR MARKINGS (100% IDENTICAL IN ALL SHOTS): Exactly match Reference Image 1 (Nini the calico cat). The head/forehead has light orange/ginger tabby fur patches with small tiger stripes, white snout/lower face, pink nose, and white chest. NO heavy solid black patches on forehead or ears. MUST match Shot 1 and Shot 3 fur coloring.
- EXACT BACKGROUND LAYOUT (100% IDENTICAL IN ALL SHOTS):
  - Viewer's LEFT background: Professional stainless steel espresso machine.
  - Viewer's RIGHT background: Dark wooden shelves with coffee bean bags and glass jars, hanging amber Edison bulb lights with soft golden bokeh.
  - Ambient moka_cat_12s warm golden lighting.
- PROP COUNT — EXACTLY ONE OF EACH, NEVER DUPLICATED: There is exactly ONE POS machine, ONE Moka pot, ONE white ceramic mug, and ONE small milk pitcher in the ENTIRE scene at all times. Each prop has a single physical instance that moves between the cat's paws and the counter across shots — it is NEVER shown in two places at once. If a prop is currently being held in a paw (the mug, the Moka pot, the milk pitcher, or the POS machine), its usual counter spot for that prop is EMPTY in that shot — do NOT also draw it resting on the counter at the same time. Before finishing each image, double check: count each prop type and confirm only one instance of it exists anywhere in the frame.
- MILK PITCHER MATERIAL (100% IDENTICAL IN ALL SHOTS): The milk pitcher is a small, OPAQUE white ceramic/ enamel pitcher with a pouring spout and small handle — the SAME matte ceramic material and opacity as the mug, in every single shot. It is NEVER drawn as a transparent/see-through glass, and its opacity, color, and finish never vary between shots.
- NO PROP MAY APPEAR OUT OF NOWHERE (CRITICAL): every prop that is used in ANY shot — the POS machine, the Moka pot, the mug, AND the milk pitcher — MUST already be visibly sitting on the counter starting in SHOT 1, even before it is used. A prop is never allowed to be introduced for the first time in Shot 2, 3, or 4. Shot 1 shows all four props laid out on the counter (the milk pitcher is simply unused and untouched at this point).
- EXACT COUNTERTOP OBJECT PLACEMENT WHEN RESTING (VIEWER'S PERSPECTIVE) — applies only when a prop is not currently being held:
  - Far LEFT counter: POS Machine resting spot.
  - CENTER counter: white ceramic mug, with the small milk pitcher sitting right next to it.
  - Far RIGHT counter: Bialetti Moka Express pot (black handle strictly on RIGHT side, mustache man logo on front).
- CAT-TO-PROP SCALE RATIO (IDENTICAL REAL-WORLD SIZE ACROSS ALL SHOTS): Cat Nini's actual body size never changes between shots. The wooden counter edge always reaches Nini's lower ribcage/belly, and the Moka pot's height is always about 45% of Nini's head-to-shoulder height. A closer camera framing (e.g. a close-up shot) is only a ZOOM/CROP change — it must NOT be drawn as if the cat, counter, or props physically grew larger; the proportions between cat, counter, and props stay mathematically identical in every shot.
- CAT APPEARANCE & CLOTHING: Exactly match Reference Image 1 (Nini the calico cat) wearing the EXACT SAME brown leather work apron with neck strap and front pocket, plus the EXACT SAME round employee ID tag on a cord necklace, in ALL shots.
- POS MACHINE APPEARANCE: Light grey front casing, glowing green screen at top, 3x4 numeric button grid layout. EXACT SAME shape, size, and color in every shot regardless of whether it is held or resting.
- ONE white ceramic mug. NEVER changes shape, size, or style.
- All objects obey gravity. Nothing floats. Nothing duplicates.
=== END CONSTRAINTS ===
"""

# 分鏡清單：每一段是一個 dict
SHOTS = [
    {
        "id": "shot1",
        "title": "Shot 1（0–4s）：刷卡付款",
        "description": "矮矮嬌小的妮妮穿棕圍裙，右爪持 POS 機（畫面左側）遞向鏡頭，綠燈確認後準備製作咖啡",
        "prompt": """Photorealistic 3D rendered storyboard frame. A gentle calico cat named Nini
(white fur with orange/ginger tabby head patches, green eyes, white chest, pink nose, short compact body height and torso),
a PART-TIME CAFE EMPLOYEE (not a customer), wearing a brown leather work apron and a round employee ID tag on a cord necklace,
standing on the STAFF side behind a dark warm wooden barista counter inside a cozy ambient cafe, at work.
BACKGROUND LAYOUT (STRICT): Professional stainless steel espresso machine on viewer's LEFT background; dark wooden shelves with coffee bags and glass jars on viewer's RIGHT background; hanging amber Edison bulb lights with golden bokeh.
COUNTERTOP LAYOUT: Center has ONE empty white ceramic mug, with ONE small opaque white ceramic milk pitcher (matte ceramic, NOT glass/transparent) sitting right next to it, untouched and unused for now. Far RIGHT counter has ONE small classic Bialetti Moka Express octagonal aluminum Moka pot (mustache man logo on front, black handle strictly on RIGHT side). ALL props that will ever appear in this story (POS machine, mug, milk pitcher, Moka pot) are already visible here in Shot 1 — nothing will be introduced later that isn't already on this counter.
POS MACHINE: The cat holds ONE light grey POS card reader with glowing green screen up with its right paw on viewer's LEFT toward the camera.
Green confirmation light glows on POS screen. Cat expression is professional and friendly.
Cinematic warm golden cafe lighting, 8K fur texture.""",
    },
    {
        "id": "shot2",
        "title": "Shot 2（4–8s）：倒咖啡，眼神飄向牛奶",
        "description": "妮妮穿棕圍裙，左爪握摩卡壺把手倒咖啡，但眼神悄悄飄向旁邊的牛奶罐，露出渴望的神情",
        "prompt": """WARNING ABOUT THE REFERENCE ANCHOR IMAGE: the master anchor image (Shot 1) shows FOUR objects sitting on the counter (POS, mug, milk pitcher, Moka pot). Copy ONLY its wall color, shelf style, lighting color/warmth, wood tones, and the cat's character design from that reference — do NOT copy its countertop object arrangement. This shot's countertop arrangement is DIFFERENT and is specified fully below; follow the list below, not the reference image's counter.

COUNT CHECK — the counter surface in this image holds EXACTLY 3 objects, no more:
  Object 1 (far left): the POS card reader, resting.
  Object 2 (center): the white ceramic mug, resting, receiving a pour of dark espresso from the Moka pot above it.
  Object 3 (right of the mug): the small opaque white ceramic milk pitcher, resting.
That is the complete list. There is NO 4th object on the counter — specifically, do NOT add a second mug, a second cup, or a second Moka pot anywhere on the counter. The Moka pot itself is NOT on the counter at all in this shot — it is being held up in the cat's paw, off the counter surface, mid-pour.

Photorealistic 3D rendered storyboard frame. Continuation from Shot 1. Copy the master anchor image's background, lighting, wood tones, and character design exactly.
The cat's forehead is entirely light orange/ginger tabby fur with small tiger stripes. White snout, pink nose, white chest, green eyes. WEARING THE EXACT SAME BROWN LEATHER WORK APRON WITH NECK STRAP AND FRONT POCKET, plus the SAME round employee ID tag on a cord necklace. She is a part-time cafe employee at work behind the staff counter, not a customer.
BACKGROUND LAYOUT (EXACT SAME AS SHOT 1): Professional stainless steel espresso machine on viewer's LEFT background; dark wooden shelves with coffee bags on viewer's RIGHT background; hanging amber Edison lights with golden bokeh.
ACTION: The cat's LEFT PAW (viewer's RIGHT) holds the ONLY Moka pot in the scene by its RIGHT-side black handle, held up above the counter, tilted, pouring a stream of dark espresso down into Object 2 (the mug). The cat's other paw is empty, resting at her side, holding nothing and touching nothing.
MOKA POT DETAILS: Bialetti mustache-man mascot logo and BIALETTI text visible on the front. Black handle strictly on the RIGHT side.
EXPRESSION: The cat's eyes drift sideways toward Object 3 (the milk pitcher) with a longing, tempted expression — a gentle internal struggle between duty and desire. Slight cheek flush of temptation.
Cinematic warm golden cafe lighting, 8K calico fur detail.""",
    },
    {
        "id": "shot3",
        "title": "Shot 3（8–12s）：倒牛奶拉花的同時忍不住偷喝一口",
        "description": "妮妮拿牛奶壺往杯裡倒奶泡拉愛心的同時，忍不住把壺嘴湊到嘴邊偷喝一口，嘴角沾著奶、瞇眼陶醉，牛奶仍在倒",
        "prompt": """Photorealistic 3D rendered storyboard frame. Continuation from Shot 2. Close-up or medium shot (a camera zoom only — Nini's actual body size and her proportions relative to the counter and props are IDENTICAL to Shot 1 and Shot 2, just framed closer).
The cat's forehead is entirely light orange/ginger tabby fur. White snout, pink nose, white chest, green eyes. WEARING THE EXACT SAME BROWN LEATHER WORK APRON, plus the SAME round employee ID tag on a cord necklace. She is a part-time cafe employee at work behind the staff counter, not a customer.
BACKGROUND LAYOUT (EXACT SAME AS SHOT 1 & 2): Professional stainless steel espresso machine on viewer's LEFT background; dark wooden shelves on viewer's RIGHT background; hanging amber Edison lights with golden bokeh.
COUNTERTOP LAYOUT:
- Far LEFT counter: The EXACT SAME light grey POS machine rests on the far-left counter corner, untouched.
- Far RIGHT counter: The EXACT SAME small Bialetti Moka pot now rests back on its far-right counter spot (set down after Shot 2's espresso pour), untouched.
- CENTER counter: The white ceramic mug (already holding dark espresso poured in Shot 2) sits stationary in the center, currently receiving a stream of milk.
- Cat holds the ONLY milk pitcher (the SAME opaque white ceramic pitcher present since Shot 1, NOT glass) in one paw, tilted, actively pouring a stream of milk into the mug to create heart latte art. The pitcher's usual counter spot is EMPTY right now since it is being held — do NOT also draw it resting on the counter.
ACTION (the pour and the secret sip happen AT THE SAME TIME — do not separate them into two moments): WHILE she is still mid-pour, with the milk stream still visibly flowing from the pitcher spout into the mug, Nini leans her head down and sneaks the pitcher's spout to her mouth for a quick secret sip/lick without stopping the pour. Her eyes are closed in pure bliss. A tiny drop of white milk is visible on her pink nose and the corner of her mouth. Expression: the perfect mix of guilty pleasure and satisfaction — blushing cheeks, a suppressed happy smile, slightly hunched posture as if hoping nobody saw — all while the pitcher is still tilted and pouring.
Soft warm golden cinematic lighting, 8K calico fur detail.""",
    },
    {
        "id": "shot4",
        "title": "Shot 4（12–16s）：假裝沒事，捧咖啡遞給客人",
        "description": "妮妮迅速恢復職業笑容，嘴角還帶著一點點奶漬，雙爪捧著拉花咖啡遞向鏡頭，帶著甜蜜又有點心虛的笑容",
        "prompt": """Photorealistic 3D rendered storyboard frame. Final shot. Close-up inside cozy ambient cafe (a camera zoom only — Nini's actual body size and her proportions relative to the counter and props are IDENTICAL to the previous shots, just framed closer).
The cat's forehead is entirely light orange/ginger tabby fur. White snout, pink nose, white chest, bright green eyes. WEARING THE EXACT SAME BROWN LEATHER WORK APRON, plus the SAME round employee ID tag on a cord necklace. She is a part-time cafe employee at work behind the staff counter, not a customer.
BACKGROUND LAYOUT (EXACT SAME AS ALL PREVIOUS SHOTS): Professional stainless steel espresso machine on viewer's LEFT background; dark wooden shelves on viewer's RIGHT background; hanging amber Edison lights with golden bokeh.
COUNTERTOP LAYOUT:
- Far LEFT counter: The EXACT SAME light grey POS machine rests on the far-left counter corner. The POS machine is resting untouched, upright on the counter.
- CENTER counter: The mug's usual spot is now EMPTY (the mug itself is being held, see below); the SAME opaque white ceramic milk pitcher from Shot 1-3 has been set back down there, now empty/nearly empty after pouring. Cat holds the ONLY white ceramic mug (the same one from Shot 1-3) with a beautiful heart latte art on top with BOTH PAWS, extending it warmly toward the viewer. BOTH of her paws are occupied ONLY with this mug — she is NOT holding the POS machine, the milk pitcher, or any other object. Do NOT draw a second mug anywhere on the counter.
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

