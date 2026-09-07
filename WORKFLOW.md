# 🎬 AI 影片生成標準作業流程 (SOP)

> 每次製作新影片前，請依照此流程執行，最大化減少 API 配額消耗。

---

## 📋 流程總覽

```
Step 1  撰寫腳本           → prompts/ 目錄
Step 2  生成分鏡確認圖     → storyboard_generator.py（免費，不消耗影片配額）
Step 3  瀏覽器確認分鏡圖   → storyboards/storyboard_preview.html
Step 4  修改直到滿意       → 重新執行 storyboard_generator.py（仍免費）
Step 5  提交影片生成任務   → 每段消耗 1 次 RPD（每天上限 10 次）
Step 6  拼接最終影片       → python concat_videos.py
Step 7  推送至 GitHub      → git push
```

---

## 📁 專案目錄結構

```
CatAnimation/
├── prompts/                        # 腳本資料夾
│   ├── chengcheng_12s_v7_shots.md  # 最新腳本（3×4s 分鏡）
│   └── ...
├── storyboards/                    # 分鏡確認圖（自動生成）
│   ├── shot1_YYYYMMDD_HHMMSS.png
│   ├── shot2_YYYYMMDD_HHMMSS.png
│   ├── shot3_YYYYMMDD_HHMMSS.png
│   └── storyboard_preview.html     # 瀏覽器預覽頁面
├── storyboard_generator.py         # ⭐ 分鏡圖生成工具（本 SOP 核心）
├── concat_videos.py                # 影片拼接工具
├── shot1.mp4 / shot2.mp4 / shot3.mp4  # 生成的影片段落
└── chengcheng_final_12s.mp4        # 最終拼接成品
```

---

## ✏️ Step 1：撰寫腳本

在 `prompts/` 目錄建立新的 `.md` 腳本檔案，參考 `chengcheng_12s_v7_shots.md` 的格式：

```markdown
## 全局硬性規則（HARD CONSTRAINTS）
...

## Shot 1（x–xs）：場景描述
- 中文分鏡說明
- English Prompt

## Shot 2 ...
## Shot 3 ...
```

> ⚠️ 撰寫 `GLOBAL_CONSTRAINTS` / 每段 prompt 時，務必檢查下方「必加硬性規則」，缺一不可。

---

## ⚠️ 必加硬性規則（每次新腳本都要包含）

每次新增 `storyboard_generator.py` 的 `GLOBAL_CONSTRAINTS`，以及 `generate_nini_video.py` / `submit_veo_jobs.py` 的每一段影片 prompt，都要包含以下規則：

| 規則 | 內容 | 目的 |
|------|------|------|
| **道具一致性** | 所有道具（POS 機、摩卡壺、馬克杯、牛奶罐等）在每一幕的**顏色、角度、形狀、高矮比例**都必須完全一致，不能換面、不能變大小 | 避免分鏡之間道具穿幫、大小不一 |
| **引力／實體接觸** | 沒被貓爪拿著的道具，底面必須完整貼合在吧台桌面上，不能懸空、飄浮、或穿透桌面；被抓握的道具要有明確的爪子接觸 | 這是地球，有引力，道具不能無故懸空 |
| **情緒自然度** | 貓咪的動作與表情要符合情境、自然合理，除非劇情明確需要，避免不必要的緊張、心虛、罪惡感等負面轉折 | 保持角色可愛親切的整體調性 |
| **主影格鏈接（Master Anchor）** | Shot 1 生成後鎖定為基準影格，後續每個 shot 都要附上這張圖作為參考，確保背景／貓咪外觀／道具 100% 一致 | `storyboard_generator.py` 已內建此機制，新腳本沿用即可 |

範例寫法（加在 `GLOBAL_CONSTRAINTS` 或影片 prompt 中）：

```
- PROP CONSISTENCY (COLOR / ANGLE / SHAPE / HEIGHT): 所有道具在每一幕都要保持完全相同的顏色、角度、形狀、高度比例。
- GRAVITY / PHYSICAL CONTACT: 沒被抓握的道具必須完整貼在桌面上，不能懸空或飄浮。
```

---

## 🖼️ Step 2：生成分鏡確認圖

1. 打開 `storyboard_generator.py`
2. 修改頂部的 `PROJECT_NAME`、`GLOBAL_CONSTRAINTS`、`SHOTS` 清單
3. 執行：

```bash
python storyboard_generator.py
```

4. 開啟瀏覽器預覽：

```bash
start storyboards/storyboard_preview.html
```

---

## ✅ Step 3–4：確認與修改分鏡圖

在 HTML 預覽頁面逐一確認：

| 確認項目 | 說明 |
|---------|------|
| 道具位置 | 摩卡壺把手右側？杯子位置正確？ |
| 道具唯一性 | 每種道具只出現一次？ |
| 道具一致性 | 跟前一幕比較，顏色、角度、形狀、高矮是否完全一致？ |
| 物理合理性 | 道具是否都貼合在桌面上，沒有懸空、飄浮？ |
| 貓咪外觀 | 顏色、眼睛、圍裙正確？ |
| 情緒表現 | 表情與動作是否自然合理，沒有不必要的緊張/罪惡感？ |
| 整體視覺 | 風格符合 IG 動畫期望？ |

**不滿意** → 修改 `SHOTS` 中的 `prompt` → 重新執行 Step 2（**完全免費！**）  
**滿意** → 進入 Step 5

---

## 🎬 Step 5：提交影片生成任務

> ⚠️ **每天上限 10 次（RPD = 10）**，請確認分鏡圖後再執行！

告知 Antigravity AI：「依照 v7 腳本生成影片，Shot 1 / Shot 2 / Shot 3」

每段生成完成後存為：
- `shot1.mp4`
- `shot2.mp4`
- `shot3.mp4`

---

## ✂️ Step 6：拼接最終影片

```bash
python concat_videos.py
# 自動偵測 shot1/2/3.mp4 → 輸出 chengcheng_final_12s.mp4
```

---

## 🚀 Step 7：推送至 GitHub

```bash
git add .
git commit -m "feat: add vX final animation"
git push origin main
```

---

## 💡 省配額小技巧

| 技巧 | 說明 |
|------|------|
| 分鏡圖確認後再拍 | 最有效，每次圖片確認省下 1–3 次影片重拍 |
| 分鏡拆 3×4s | 只重拍有問題的那段，不用整個 12s 重來 |
| 首末幀鎖定 | 用 Shot N 的最後一幀當 Shot N+1 的首幀輸入 |
| 硬性規則區塊 | 每段 prompt 最頂部放 CONSTRAINTS，AI 優先遵守 |
| 道具一致性 + 引力規則 | 每次新腳本都套用「必加硬性規則」，避免道具懸空、變形、換角度導致重拍 |
| 確認帳單餘額 | 每天生成前先到 [AI Studio Rate Limit](https://aistudio.google.com) 確認剩餘 RPD |
