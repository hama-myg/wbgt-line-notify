import os, re, math, requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone, timedelta

# ---- 1. tenki.jp 熱中症情報（掛川市）を取得 -------------------
URL = "https://tenki.jp/heatstroke/5/25/5040/22213/"

html = requests.get(
    URL,
    headers={"User-Agent": "Mozilla/5.0"},  # UAを付けてブロック回避
    timeout=15
).text
soup = BeautifulSoup(html, "lxml")

# ---- 2. 「今日の最高：xx.x℃以上yy.y℃未満」を探す ------------
m = re.search(
    r"今日の最高：\s*(\d+(?:\.\d+)?)℃以上(\d+(?:\.\d+)?)℃未満",
    soup.get_text()
)

if not m:
    raise RuntimeError("WBGTレンジが取れませんでした。ページ構造が変わった可能性")
low, high = map(float, m.groups())
wbgt_max = round(high - 0.1, 1)   # 上限値 -0.1℃ を擬似最高値とする

# ---- 3. 注意コメントを生成 ------------------------------------
if wbgt_max < 25:
    advice = "通常作業可。ただし水分補給を励行し、適宜休憩を。"
elif wbgt_max < 28:
    advice = "⚠️警戒：作業強度に応じて1時間に1回以上休憩を推奨。"
elif wbgt_max < 31:
    advice = "⚠️厳重警戒：負荷軽減＋30分ごとに日陰/冷房休憩必須。"
else:
    advice = "🚨危険：空調服必須、30分ごとに冷所休憩と水分補給！"

print(f"本日のWBGT最高予想は{wbgt_max}℃です。\n" + advice)
