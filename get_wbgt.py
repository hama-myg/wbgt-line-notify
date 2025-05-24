import csv, datetime, requests

# ---- 1. 今日の日付と静岡県メッシュID ----
today = datetime.date.today().strftime("%Y%m%d")
mesh_id = "50331"  # 掛川市に最も近い静岡地点
url = f"https://www.wbgt.env.go.jp/record_data_download.php?sid={mesh_id}&date={today}"

# ---- 2. CSVを取得し最高WBGTを抽出 ----
rows = csv.reader(requests.get(url, timeout=15).text.splitlines())
next(rows)               # ヘッダー行を飛ばす
wbgt_max = max(float(r[2]) for r in rows if r[2])

# ---- 3. コメント生成 ----
if wbgt_max < 25:
    advice = "通常作業可。ただし水分補給を励行し、適宜休憩を。"
elif wbgt_max < 28:
    advice = "⚠️警戒：1時間に1回以上休憩を推奨。"
elif wbgt_max < 31:
    advice = "⚠️厳重警戒：30分ごとに冷所休憩必須。"
else:
    advice = "🚨危険：空調服必須、30分ごとに冷所休憩と水分補給！"

print(f"本日のWBGT最高予想は{wbgt_max:.1f}℃です。\\n" + advice)
