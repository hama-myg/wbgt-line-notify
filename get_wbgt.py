import csv, requests

CSV_URL = "https://www.wbgt.env.go.jp/prev15WG/dl/yohou_50551.csv"
csv_lines = requests.get(CSV_URL, timeout=15).text.splitlines()
reader = list(csv.reader(csv_lines))

# 2行目が本データ行（確定）
data_row = reader[1]

# 3列目以降のWBGT値（文字列） → 10分の1にしてfloat化
wbgt_values = []
for val in data_row[2:2+48]:  # ← 2列目からスタートして48個だけ見る
    try:
        num = float(val.strip()) / 10  # ← ここで10分の1に補正
        if 0 < num < 60:               # 現実的なWBGT範囲
            wbgt_values.append(num)
    except ValueError:
        continue

if not wbgt_values:
    raise RuntimeError("WBGT値が取得できませんでした（全データが無効）")

wbgt_max = round(max(wbgt_values), 1)

# 注意レベルメッセージ
if wbgt_max < 25:
    advice = "・25℃未満：通常作業可。ただし水分補給を励行し、適宜休憩を"
elif wbgt_max < 28:
    advice = "・25℃〜28℃未満：警戒レベル。作業強度に応じて1時間に1回以上の休憩を推奨"
elif wbgt_max < 31:
    advice = "・28℃〜31℃未満：厳重警戒レベル。作業負荷軽減＋30分に1回以上の休憩。日陰や冷房下での休憩必須"
else:
    advice = "・31℃以上：危険レベル。空調服必須、30分に1回以上エアコンやミストファンが設置された場所での休憩を行い、都度水分補給"

# 出力（Slackや他サービスに送信される内容）
print(f"本日のWBGT最高予想は{wbgt_max}℃です。\n{advice}")
