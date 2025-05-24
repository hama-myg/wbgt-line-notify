import csv, datetime, requests

# ---- 1. きょうの日付文字列 -------------------------------
today = datetime.date.today()               # 例: 2025-05-24
today_str = today.strftime("%Y-%m-%d")      # CSV の日付形式

# ---- 2. 掛川市（地点 50551）の 3 日間予測 CSV を取得 -------
CSV_URL = "https://www.wbgt.env.go.jp/prev15WG/dl/yohou_50551.csv"
csv_text = requests.get(CSV_URL, timeout=15).text.splitlines()

# ---- 3. 当日行だけ抽出し、最高 WBGT を求める -------------
reader = csv.DictReader(csv_text)
wbgt_today = [
    float(row["WBGT"])                       # 列名は「WBGT」
    for row in reader
    if row["日付"] == today_str and row["WBGT"]
]
if not wbgt_today:
    raise RuntimeError("本日のデータが取得できませんでした。CSV 仕様変更の可能性")

wbgt_max = round(max(wbgt_today), 1)

# ---- 4. 注意コメントを生成 -------------------------------
if wbgt_max < 25:
    advice = "通常作業可。ただし水分補給を励行し、適宜休憩を。"
elif wbgt_max < 28:
    advice = "⚠️警戒：1時間に1回以上休憩を推奨。"
elif wbgt_max < 31:
    advice = "⚠️厳重警戒：負荷軽減＋30分ごとに冷所休憩必須。"
else:
    advice = "🚨危険：空調服必須、30分ごとに冷所休憩と水分補給！"

print(f"本日のWBGT最高予想は{wbgt_max}℃です。\n" + advice)
