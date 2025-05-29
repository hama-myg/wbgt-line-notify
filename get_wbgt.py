import csv
import requests
from datetime import datetime, timedelta

# --- 現在日付を取得（JST） ---
today = (datetime.utcnow() + timedelta(hours=9)).strftime("%Y%m%d")  # 例：'20240529'

# --- CSV読み込み ---
CSV_URL = "https://www.wbgt.env.go.jp/prev15WG/dl/yohou_50551.csv"
response = requests.get(CSV_URL, timeout=15)
response.encoding = 'utf-8'  # 文字コードを指定
csv_lines = response.text.splitlines()
reader = list(csv.reader(csv_lines))

header = reader[0]
data_row = reader[1]

# --- ヘッダーの日付から「今日のWBGT列」のインデックスを取得 ---
today_indexes = [
    i for i, col in enumerate(header)
    if col.startswith(today) and i < len(data_row)
]

# --- 今日のWBGT値のみを取得 ---
wbgt_values = []
for i in today_indexes:
    try:
        num = float(data_row[i].strip()) / 10
        if 0 < num < 60:
            wbgt_values.append(num)
    except ValueError:
        continue

if not wbgt_values:
    raise RuntimeError("今日のWBGT値が取得できませんでした（全データが無効）")

wbgt_max = round(max(wbgt_values), 1)

# --- 注意レベルメッセージ ---
if wbgt_max < 25:
    advice = "通常作業可。ただし水分補給を励行し、適宜休憩を。"
elif wbgt_max < 28:
    advice = "⚠️警戒：1時間に1回以上休憩を推奨。"
elif wbgt_max < 31:
    advice = "⚠️厳重警戒：30分ごとに冷所休憩必須。"
else:
    advice = "🚨危険：空調服必須、30分ごとに冷所休憩と水分補給！"

print(f"本日（{today}）のWBGT最高予想は {wbgt_max}℃ です。\n{advice}")
