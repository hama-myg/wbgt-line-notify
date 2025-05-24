import csv, requests

CSV_URL = "https://www.wbgt.env.go.jp/prev15WG/dl/yohou_50551.csv"
csv_lines = requests.get(CSV_URL, timeout=15).text.splitlines()
reader = list(csv.reader(csv_lines))
print("DATA ROW:", reader[1][:8])


# ヘッダー確認（任意ログ）
print("HEADER:", reader[0][:5])  # 最初の5列だけ表示

# 2行目が実データ（1地点のみ）
data_row = reader[1]

# 3列目以降（WBGT値）から安全に数値だけ抽出
wbgt_values = []
for val in data_row[2:]:
    try:
        num = float(val)
        if 0 < num < 60:   # 常識的なWBGT範囲（例：0〜60℃）
            wbgt_values.append(num)
    except ValueError:
        continue

if not wbgt_values:
    raise RuntimeError("WBGT値が取得できませんでした（全データが無効）")

wbgt_max = round(max(wbgt_values), 1)

# メッセージ生成
if wbgt_max < 25:
    advice = "通常作業可。ただし水分補給を励行し、適宜休憩を。"
elif wbgt_max < 28:
    advice = "⚠️警戒：1時間に1回以上休憩を推奨。"
elif wbgt_max < 31:
    advice = "⚠️厳重警戒：30分ごとに冷所休憩必須。"
else:
    advice = "🚨危険：空調服必須、30分ごとに冷所休憩と水分補給！"

print(f"本日のWBGT最高予想は{wbgt_max}℃です。\n{advice}")
