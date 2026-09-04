# 🐱 黑貓「丞丞」分鏡三段式腳本 (v7 - 3×4s Shot Design)

> **主角：** 黑貓丞丞（全黑色、翡翠綠眼睛、棕色皮革圍裙）
> **風格：** 寫實 3D 電影級質感 (Photorealistic Cinematic 3D)
> **策略：** 每段 4 秒獨立生成，後期拼接為 12 秒完整影片
> **優點：** 短 prompt 讓 AI 更容易維持道具一致性與物理正確性

---

## 🔒 全局硬性規則（每段 prompt 都必須套用）

```
=== HARD CONSTRAINTS (NEVER VIOLATE) ===
- ONE white ceramic mug. Rests on counter. NEVER changes shape, size, or style.
- Moka pot: octagonal metal body. Black handle on RIGHT SIDE ONLY. Never left. Never changes shape.
- POS card machine: stays visible on LEFT side of counter at ALL times.
- Cat does NOT start coffee-making until AFTER green payment light confirms.
- All objects obey gravity. Nothing floats.
=== END CONSTRAINTS ===
```

---

## 🎬 Shot 1 (0–4 秒)：索卡付款 ➔ 確認後放下 POS 機

### 場景配置
```
吧台配置（左到右）：
[左] POS 信用卡機  |  [中] 空白瓷馬克杯（空的）  |  [右] 八角形金屬摩卡壺（黑色把手朝右）
```

### 中文分鏡
```
- 黑貓丞丞右爪拿起 POS 機，遞向鏡頭索取信用卡。
- 顧客信用卡感應 POS 機（綠燈亮起確認付款成功）。
- 丞丞確認付款後，將 POS 機放回吧台左側（留在畫面中）。
- Shot 結束時：POS 機在左側，空白杯在中間，摩卡壺在右側。
```

### 🇺🇸 English Prompt (Shot 1 - 4 seconds)
```
=== HARD CONSTRAINTS (NEVER VIOLATE) ===
- ONE white ceramic mug on counter center. NEVER changes shape.
- Octagonal metal Moka pot, black handle RIGHT SIDE ONLY, NEVER changes shape.
- POS machine stays visible LEFT side counter ALL times.
- Cat does NOT touch coffee equipment until green light confirms payment.
- All objects obey gravity. Nothing floats.
=== END CONSTRAINTS ===

Photorealistic 3D animation, 4 seconds. Sleek black cat with emerald green eyes and brown leather apron stands behind a wooden counter.
Counter layout: POS card machine on far left, ONE empty white ceramic mug in center, octagonal metal Moka pot with black handle on right.
The cat picks up the POS machine with its right paw and holds it out toward the camera/viewer.
A credit card taps the device. A green confirmation light flashes on the screen.
ONLY AFTER the green light: the cat nods and places the POS machine back onto the far left of the counter where it remains visible.
Shot ends with cat's paws moving toward the Moka pot to begin brewing.
Cinematic 3D lighting, 8K black fur texture, strict prop permanence.
```

---

## 🎬 Shot 2 (4–8 秒)：摩卡壺倒咖啡 ➔ 奶泡拉花

### 場景配置（延續 Shot 1 結束狀態）
```
吧台配置（左到右）：
[左] POS 機（靜置，全程可見）  |  [中] 空白白瓷杯（靜置在吧台上）  |  [右] 摩卡壺（黑把手朝右）
```

### 中文分鏡
```
- 丞丞填入咖啡粉至摩卡壺粉槽，鎖緊壺身，置於爐火上加熱，深色咖啡開始升至上壺。
- 丞丞右手握住摩卡壺右側黑色把手，傾斜壺身（造型不變，僅角度改變），
  將深色濃縮咖啡倒入「吧台中央同一個白瓷杯」中。
- 放下摩卡壺，拿起奶泡壺，將白色綿密奶泡倒入「同一個杯子（未移動未更換）」，拉出愛心拉花。
- Shot 結束時：愛心拉花完成，POS 機仍在左側，杯子靜置中央，摩卡壺在右側。
```

### 🇺🇸 English Prompt (Shot 2 - 4 seconds)
```
=== HARD CONSTRAINTS (NEVER VIOLATE) ===
- The white ceramic mug from Shot 1 is the EXACT SAME mug here. Stationary on counter center. NEVER floats.
- Moka pot: same octagonal metal body, black handle RIGHT SIDE ONLY, shape never changes.
- POS machine: remains visible on far LEFT of counter throughout.
- All objects obey gravity.
=== END CONSTRAINTS ===

Photorealistic 3D animation, 4 seconds. Continuation from previous shot.
Counter layout: POS machine on far left (visible), ONE white ceramic mug stationary in center, Moka pot with right-side black handle on right.
The black cat fills coffee grounds into the Moka pot, screws it shut, and heats it on a small stove. Steam rises as dark espresso brews.
The cat grips the Moka pot by its RIGHT-SIDE black handle, tilts it (shape unchanged, angle only), and pours dark espresso into the STATIONARY white ceramic mug on the counter.
Cat sets down the Moka pot, picks up a milk pitcher, and pours steamed white milk into the SAME white mug, creating a heart-shaped latte art.
Cinematic 3D lighting, 8K black fur texture, strict prop permanence.
```

---

## 🎬 Shot 3 (8–12 秒)：雙爪端起 ➔ 偷喝奶泡 ➔ 瞇眼害羞笑遞給你

### 場景配置（延續 Shot 2 結束狀態）
```
吧台配置：
[左] POS 機（靜置可見）  |  [中] 完成拉花的白瓷杯  |  [右] 摩卡壺（放回原位）
```

### 中文分鏡
```
- 丞丞雙爪從吧台上捧起「完成愛心拉花的同一個白瓷杯」，準備遞給顧客。
- 就在快要遞出的瞬間，丞丞忍不住湊近杯口，用粉紅色小舌頭偷偷舔了一口奶泡。
- 驚覺鏡頭在拍，丞丞緩緩抬起頭。
- 翡翠綠眼睛害羞地瞇成月牙形，嘴角上揚甜甜微笑。
- 雙爪捧著「同一個拉花白瓷杯（奶泡略少）」直接遞向螢幕前的你。
```

### 🇺🇸 English Prompt (Shot 3 - 4 seconds)
```
=== HARD CONSTRAINTS (NEVER VIOLATE) ===
- The SAME white ceramic mug from Shot 1 and 2. Heart latte art visible on top. Shape never changes.
- POS machine: still visible on far left counter.
- All objects obey gravity. Mug held by cat's paws, never floats on its own.
=== END CONSTRAINTS ===

Photorealistic 3D animation, 4 seconds. Continuation from previous shot.
The black cat with emerald green eyes lifts the SAME white ceramic mug (with heart latte art) from the counter using both paws.
As the cat begins to hand the mug toward the camera, it pauses and stealthily licks a tiny bit of milk foam from the top with its small pink tongue.
The cat slowly looks up, realizes it has been caught on camera.
Its emerald green eyes gently squint into happy crescent moon shapes. A warm, bashful smile forms on its face.
The cat holds the SAME mug (foam slightly reduced from the sip) directly out toward the viewer with both paws.
Close-up shot, soft warm lighting, cinematic 3D, 8K black fur texture.
```

---

## ✂️ 後期拼接指令

三段影片生成完成後，使用以下指令拼接：

```bash
python concat_videos.py
# 輸入：shot1.mp4, shot2.mp4, shot3.mp4
# 輸出：chengcheng_final_12s.mp4
```

---

## 📊 版本歷史

| 版本 | 說明 | 影片長度 |
|------|------|---------|
| v1 | 初版黑貓丞丞 | 12s 單段 |
| v2 | 摩卡壺方向與杯子修正 | 12s 單段 |
| v3 | 道具一致性強化 | 12s 單段 |
| v4 | 物理重力與索卡觸發 | 12s 單段 |
| v5 | POS 機常駐 + 把手鎖右側 | 12s 單段 |
| v6 | 杯子唯一性 + 付款觸發邏輯 | 12s 單段 |
| **v7** | **3×4s 分鏡策略 + 硬性規則區塊** | **4s + 4s + 4s → 拼接 12s** |

*最後更新：2026-09*
