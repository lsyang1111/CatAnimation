# 🐱 寫實 3D 貓咪咖啡廳店員動畫 Prompt (12 秒非吉卜力風格)

> **場景總覽：** 12 秒超寫實 3D 貓咪店員動畫。貓咪專注打奶泡 -> 趁不注意偷喝奶泡被抓包 -> 裝可憐捧咖啡遞給顧客。

---

## 📌 畫面與鏡頭時間規劃 (12 秒 Storyboard & Timing)

- **Shot 1 (0.0s - 4.0s)：吧台專注打奶泡**
  - **鏡頭：** 中景 (Medium Shot)，慢速推進 (Dolly In)。
  - **動作：** 寫實 3D 貓咪店員站在吧台後，雙爪扶著奶泡鋼杯，蒸氣從咖啡機噴出，貓耳隨著震動微抖。

- **Shot 2 (4.0s - 8.5s)：偷喝奶泡與驚覺被發現**
  - **鏡頭：** 特寫 (Close-Up)，低角度仰拍，焦點從奶泡杯轉轉移至貓咪面部。
  - **動作：** (4.0s-6.2s) 貓咪伸出粉嫩舌頭快速舔舐奶泡，眼睛滿足地瞇成月牙狀；(6.2s-8.5s) 貓咪耳朵突然豎起，驚覺被看見，瞳孔瞬間放大，嘴邊沾著白色奶泡凍結在原地。

- **Shot 3 (8.5s - 12.0s)：委屈裝可憐遞咖啡**
  - **鏡頭：** 過肩鏡頭 (OTS) 轉雙爪特寫，微俯拍。
  - **動作：** 貓咪用兩隻小爪子將少了一小口奶泡的咖啡杯推向鏡頭/顧客，抬頭展現水汪汪大眼與微微後壓的耳朵（飛機耳），露出極致委屈無辜的表情。

---

## 🎬 Prompt 模板 (適用於 Veo 3.1 / Kling 1.5 / Runway Gen-3)

### 🎨 步驟一：靜態 3D 角色基準圖 Prompt (Text-to-Image Keyframe)

```text
Photorealistic 3D render of an adorable cream tabby cat barista, wearing a dark brown leather mini apron, standing behind a warm wooden coffee shop counter. Highly detailed individual fur strands, realistic cat facial anatomy, wet pink nose, glowing amber eyes, soft subsurface scattering on ears. Cinematic lighting, soft bokeh, Unreal Engine 5 render style, Octane Render, 8k resolution, ray-tracing reflections on stainless steel espresso machine.
```

---

### 🎬 Shot 1: Brewing & Milk Frothing (0s - 4s)

#### 中文 Prompt
```text
超寫實 3D 動畫，一隻穿著皮革小圍裙的奶油橘貓店員站在溫馨木質咖啡吧台後。貓咪認真操作義式咖啡機，蒸氣裊裊升起，雙爪穩穩扶著奶泡鋼杯。耳朵因震動微微抖動，眼神專注。電影級暖光，細緻毛髮紋理與真實物理動態，Octane Render 寫實 3D 風格，鏡頭緩慢向前推進。
```

#### English Prompt
```text
Photorealistic 3D animation, medium shot with slow dolly-in movement. A cream tabby cat barista wearing a small leather apron operates a shiny espresso machine behind a cozy wooden counter. Volumetric steam rises from the steam wand as the cat froths milk with focused eyes. Tiny vibrations twitch its ears. Hyper-detailed fur texture, subsurface scattering on cat ears, warm golden sunlight filtering through window, 3D Octane Render quality, 24fps smooth motion.
```

---

### 🎬 Shot 2: Sneak Sip & Caught Reaction (4s - 8.5s)

#### 中文 Prompt
```text
超寫實 3D 特寫鏡頭。貓咪店員悄悄將奶泡杯湊近，粉紅舌頭輕舔濃密奶泡，眼睛陶醉瞇起。突然感覺到顧客視線，貓咪瞬間豎起耳朵，雙眼睜得圓滾滾，嘴唇與鼻尖還沾著一小抹白色奶泡，驚恐又無辜地定格看著鏡頭。淺景深，細膩面部肌肉微表情，寫實 3D 動態。
```

#### English Prompt
```text
Cinematic 3D close-up shot, rack focus from the milk foam to the cat's face. The cat barista quickly laps up the velvety milk foam with its tiny pink tongue, eyes squinting in pure delight. Suddenly sensing someone watching, its ears snap straight up, its amber eyes dilate wide in shock, white milk foam sticking to its nose and whiskers. Frozen in a caught-in-the-act pause, realistic fur dynamics, photorealistic lighting, cinematic shallow depth of field.
```

---

### 🎬 Shot 3: Innocent Serve to Customer (8.5s - 12s)

#### 中文 Prompt
```text
超寫實 3D 鏡頭，從過肩鏡頭轉為貓咪正面特寫。貓咪店員用兩隻小毛爪將咖啡杯輕輕推向顧客，杯中奶泡少了一小塊。貓咪抬起頭，水汪汪大眼睛直視鏡頭，耳朵微微向後壓成飛機耳，嘴巴微抿露出無辜委屈表情。柔和溫暖燈光，真實物理質感，寫實 3D 電影畫質。
```

#### English Prompt
```text
Photorealistic 3D close-up shot, smooth pan down to cat's paws. The cat barista uses both fluffy paws to gently slide the coffee cup across the wooden counter towards the camera. The froth in the cup is noticeably missing a small sip mark. The cat tilts its head up, looking directly into the camera with huge teary glossy eyes and slightly flattened ears, forming a heart-melting innocent apology expression. Soft volumetric indoor lighting, hyper-realistic fur details, 4K resolution.
```

---

## 🚫 負面 Prompt (Negative Prompts)

```text
2D illustration, Ghibli style, anime art, cartoon, flat shading, lowpoly, distorted paws, extra fingers, uncanny valley, morphing limbs, blurry fur, jittery motion, frame drops, low resolution, overexposed.
```

---

## ⚙️ Image-to-Video (I2V) 一致性生成流程建議

1. **基準圖生成 (Keyframe Zero):** 先用 Midjourney v6 / Flux / DALL-E 3 生成靜態寫實 3D 貓咪店員圖，確保毛色、眼色、圍裙細節固定。
2. **首尾幀銜接 (Frame Chaining):**
   - Shot 1 生成後，截取第 4 秒最後一幀 (Last Frame) 作為 Shot 2 的輸入圖 (First Frame)。
   - Shot 2 生成後，截取第 8.5 秒最後一幀作為 Shot 3 的輸入圖。
3. **Motion / Camera Control 設定:**
   - Shot 1: Camera Zoom In / Push (Motion strength: 3-4)
   - Shot 2: Static Close-Up with focal shift (Motion strength: 4-5)
   - Shot 3: Downward Pan & Tilt (Motion strength: 3)
