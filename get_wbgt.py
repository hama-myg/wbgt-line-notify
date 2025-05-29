import csv
import requests
import smtplib
import os
from email.mime.text import MIMEText
from email.utils import formatdate

# --- 定数 ---
CSV_URL = "https://www.wbgt.env.go.jp/prev15WG/dl/yohou_50551.csv"
WBGT_TODAY_COUNT = 144  # 10分間隔×24時間 = 今日のデータ個数

# --- CSVからWBGT値を取得 ---
csv_lines = requests.get(CSV_URL, timeout=15).text.splitlines()
reader = list(csv.reader(csv_lines))
data_row = reader[1]  # 実データ行（1行目）

# 今日のWBGT値のみを抽出（2列目から開始）
today_values_raw = data_row[2 : 2 + WBGT_TODAY_COUNT]

wbgt_values = []
for val in today_values_raw:
    try:
        num = float(val.strip()) / 10  # WBGT値は10分の1単位
        if 0 < num < 60:
            wbgt_values.append(num)
    except ValueError:
        continue

if not wbgt_values:
    raise RuntimeError("今日のWBGT値が取得できませんでした（全データが無効）")

wbgt_max = round(max(wbgt_values), 1)

# --- 注意レベルの判定 ---
if wbgt_max < 25:
    advice = "・25℃未満：通常作業可。ただし水分補給を励行し、適宜休憩を"
elif wbgt_max < 28:
    advice = "・25℃〜28℃未満：警戒レベル。作業強度に応じて1時間に1回以上の休憩を推奨"
elif wbgt_max < 31:
    advice = "・28℃〜31℃未満：厳重警戒レベル。作業負荷軽減＋30分に1回以上の休憩。日陰や冷房下での休憩必須"
else:
    advice = "・31℃以上：危険レベル。空調服必須、30分に1回以上エアコンやミストファンが設置された場所での休憩を行い、都度水分補給"

# --- メール送信（環境変数から取得） ---
gmail_user = os.environ["GMAIL_USER"]
gmail_password = os.environ["GMAIL_APP_PASSWORD"]
to_address = os.environ["GMAIL_TO"]

subject = "【WBGT注意】本日の最高予想は " + str(wbgt_max) + "℃"
body = f"本日（0:00〜23:50）のWBGT最高予想は {wbgt_max}℃ です。\n{advice}"

msg = MIMEText(body, _charset="utf-8")
msg["Subject"] = subject
msg["From"] = gmail_user
msg["To"] = to_address
msg["Date"] = formatdate(localtime=True)

with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
    smtp.starttls()
    smtp.login(gmail_user, gmail_password)
    smtp.send_message(msg)

print("✅ WBGT Gmail 通知を送信しました。")
