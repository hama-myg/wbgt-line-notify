import csv, datetime, requests

today = datetime.date.today()
today_str = today.strftime("%Y-%m-%d")

CSV_URL = "https://www.wbgt.env.go.jp/prev15WG/dl/yohou_50551.csv"
csv_lines = requests.get(CSV_URL, timeout=15).text.splitlines()

# --- 🔍 追加ログ出力：CSVヘッダーを確認 -------------------------
print("HEADER LINE (raw):", csv_lines[0])

# --- 1. ヘッダーを動的に取得 ---------------------------------
header = next(csv.reader([csv_lines[0]]))
# date / 日付 列のインデックス（英日どちらでも可）
if "date" in header:
    idx_date = header.index("date")
    idx_wbgt = header.index("wbgt")
else:
    idx_date = header.index("日付")
    idx_wbgt = header.index("WBGT")

# --- 2. 当日行を抽出し最高WBGTを計算 -------------------------
wbgt_today = []
for row in csv.reader(csv_lines[1:]):
    if row[idx_date] == today_str and row[idx_wbgt]:
        wbgt_today.append(float(row[idx_wbgt]))

if not wbgt_today:
    raise RuntimeError("本日のデータが取得できませんでした。CSV 仕様変更?")

wbgt_max = round(max(wbgt_today), 1)

# --- 3. メッセージ生成 --------------------------------------
if wbgt_max < 25:
    advice = "通常作業可。ただし水分補給を励行し、適宜休憩を。"
elif wbgt_max < 28:
    advice = "⚠️警戒：1時間に1回以上休憩を推奨。"
elif wbgt_max < 31:
    advice = "⚠️厳重警戒：負荷軽減＋30分ごとに冷所休憩必須。"
else:
    advice = "🚨危険：空調服必須、30分ごとに冷所休憩と水分補給！"

print(f"本日のWBGT最高予想は{wbgt_max}℃です。\n{advice}")
