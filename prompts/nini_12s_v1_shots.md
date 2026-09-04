# 🐱 妮妮「三花貓打工仔」12 秒分鏡腳本 (v1)

> **主角：** 妮妮（三花貓 — 白底橘黑花紋、綠色眼睛、白色胸口）
> **個性：** 溫和可愛的母貓，不是故意偷喝，只是真的忍不住
> **風格：** 寫實 3D 電影級質感，咖啡廳打工仔場景
> **策略：** 3×4s 分鏡獨立生成後拼接

---

## 🔒 全局硬性規則

```
=== HARD CONSTRAINTS (NEVER VIOLATE) ===
- Cat character: calico cat, white fur with orange and black patches, green eyes, white chest — NEVER changes appearance.
- ONE white ceramic mug. NEVER changes shape, size, or style throughout all shots.
- Classic dark aluminum octagonal Moka pot (Bialetti-style). Black handle RIGHT SIDE ONLY. Shape never changes.
- POS card machine stays visible on LEFT side of counter at ALL times after being set down.
- Cat does NOT start coffee-making until AFTER green payment light confirms.
- All objects obey gravity. Nothing floats.
=== END CONSTRAINTS ===
```

---

## 🎬 Shot 1（0–4 秒）：索卡付款

### 中文分鏡
```
- 溫暖咖啡廳吧台（由左到右）：
  空白白瓷杯（中央）｜ 深色八角摩卡壺（右，黑把手朝右）
- 妮妮穿著棕色皮革圍裙，站在吧台後方，用右爪舉起 POS 機遞向鏡頭等待刷卡。
- 顧客信用卡感應（綠燈確認付款成功）。
- 妮妮將 POS 機放回吧台左側（全程留在畫面中），才開始製作咖啡。
```

### 🇺🇸 English Prompt (Shot 1)
```
=== HARD CONSTRAINTS (NEVER VIOLATE) ===
- Cat: calico cat, white fur with orange and black patches, green eyes, white chest. NEVER changes.
- ONE white ceramic mug on counter center. NEVER changes shape.
- Classic dark aluminum Bialetti-style Moka pot, black handle RIGHT SIDE ONLY, shape never changes.
- NO POS machine on the counter surface — cat is HOLDING the only POS machine.
- Cat does NOT touch coffee equipment until green payment light confirms.
=== END CONSTRAINTS ===

Photorealistic 3D animation, 4 seconds.
A gentle calico cat (white fur with orange and black patches, green eyes, white chest) wearing a brown leather apron
stands behind a wooden barista counter inside a cozy warm cafe.
BACKGROUND: wooden shelves with coffee bean bags, professional espresso machine, hanging Edison bulb lights, soft golden bokeh.
Counter has ONLY TWO items: ONE empty white ceramic mug in center,
ONE classic dark aluminum octagonal Moka pot (Bialetti-style, black handle on RIGHT).
NO POS machine on counter surface.
The calico cat holds ONE POS card reader up with its right paw toward the camera.
A credit card taps the device. Green confirmation light flashes.
ONLY AFTER the green light: the cat nods gently and places the POS machine on the far left of the counter.
Cinematic warm cafe lighting, 8K fur texture.
```

---

## 🎬 Shot 2（4–8 秒）：摩卡壺倒咖啡 ➔ 奶泡愛心拉花

### 中文分鏡
```
- 妮妮將咖啡粉填入摩卡壺，鎖緊壺身，置於爐火加熱，濃縮咖啡升上來。
- 右爪握住右側黑色把手，傾斜壺身（造型不變，僅角度傾斜），
  將深色濃縮咖啡倒入「吧台中央同一個白瓷杯」中。
- 放下摩卡壺，拿起奶泡壺，將白色奶泡倒入「同一個杯子」拉出愛心拉花。
```

### 🇺🇸 English Prompt (Shot 2)
```
=== HARD CONSTRAINTS (NEVER VIOLATE) ===
- Cat: SAME calico cat (white/orange/black patches, green eyes, white chest) as Shot 1.
- The white ceramic mug from Shot 1 is the EXACT SAME mug here — stationary on counter center. NEVER floats.
- Moka pot: SAME classic dark aluminum Bialetti-style, black handle RIGHT SIDE ONLY, shape never changes.
- POS machine: placed on far LEFT counter, still visible throughout.
=== END CONSTRAINTS ===

Photorealistic 3D animation, 4 seconds. Continuation from Shot 1.
SAME calico cat (white/orange/black patches, green eyes) in brown leather apron behind wooden barista counter.
BACKGROUND: same warm cafe interior — wooden shelves, espresso machine, Edison lights, golden bokeh.
Counter: POS machine on far LEFT (visible), ONE white ceramic mug STATIONARY in center.
The cat fills the dark aluminum octagonal Moka pot with coffee grounds, heats it on a small stove — steam rises.
Cat grips Moka pot by its RIGHT-SIDE black handle, tilts it (shape unchanged) and pours dark espresso
into the STATIONARY white ceramic mug.
Cat sets Moka pot down, picks up milk pitcher, pours steamed milk into the SAME mug creating heart latte art.
Cinematic warm cafe lighting, 8K fur texture.
```

---

## 🎬 Shot 3（8–12 秒）：偷舔奶泡 ➔ 楚楚可憐遞給你

### 中文分鏡
```
- 妮妮雙爪捧起「完成愛心拉花的同一個白瓷杯」準備遞給顧客。
- 奶泡太香，忍不住用粉紅小舌頭偷偷舔了一口。
- 被鏡頭抓包，慢慢抬起頭，露出最無辜、楚楚可憐的表情。
  （妮妮個性溫和，不是故意的，她只是真的太喜歡奶泡了🥺）
- 雙爪捧著「奶泡略少的同一個白瓷杯」輕輕遞向螢幕前的你。
```

### 🇺🇸 English Prompt (Shot 3)
```
=== HARD CONSTRAINTS (NEVER VIOLATE) ===
- Cat: SAME calico cat (white/orange/black patches, green eyes, white chest) as Shot 1 and 2.
- The SAME white ceramic mug with heart latte art. Shape never changes. Held by cat's paws — never floats alone.
=== END CONSTRAINTS ===

Photorealistic 3D animation, 4 seconds. Continuation from Shot 2.
Close-up shot of SAME calico cat (white/orange/black fur patches, green eyes, white chest) in brown leather apron.
BACKGROUND: warm blurred cafe interior with golden bokeh lights.
The cat lifts the SAME white ceramic mug (heart latte art on top) with BOTH PAWS to offer it to the viewer.
Just before handing it over, the cat can't resist — it gently licks a tiny sip of milk foam with its small pink tongue.
The cat slowly looks up, realizes it has been caught on camera.
Expression: NOT guilty smirk, but the most innocent, soft, doe-eyed look — 
gentle crescent-moon eyes, slightly parted mouth, a look that says "I'm sorry... but it was so good 🥺".
The cat softly extends the mug (foam slightly reduced) toward the viewer with both paws.
Soft warm cinematic lighting, 8K calico fur texture.
```

---

## 🐾 妮妮角色備忘錄

| 特徵 | 說明 |
|------|------|
| 毛色 | 白底 + 橘色斑塊 + 黑色斑塊（三花） |
| 眼睛 | 綠色 |
| 胸口 | 白色 |
| 個性 | 溫和、可愛 |
| 招牌表情 | 楚楚可憐的無辜眼神（不是壞心，只是忍不住）|
| 圍裙 | 棕色皮革圍裙 |

*最後更新：2026-09*
