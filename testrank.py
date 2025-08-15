import os
import requests
from bs4 import BeautifulSoup

# --- 1. グループ分け定義 ---
GROUPS = {
    "グループ①": ["みくろん", "うた", "えろっぴ", "あさの"],
    "グループ②": ["9292", "大村", "bago", "アンクラ"],
    "グループ③": ["gonbeyy", "kaomoji", "なしょ", "ばーす"]
}

# --- 2. Discord Webhook（環境変数から取得推奨） ---
WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
print("Webhook URL:", WEBHOOK_URL)
print("POSTメッセージ送信テスト")
res = requests.post(WEBHOOK_URL, json={"content": "Discord通知テストです！"})

print("Discord response:", res.status_code)
print("Discord response text:", res.text)

# --- 3. セッションとページ取得（ログインなし前提） ---
session = requests.Session()
pog_group_url = "https://pog.netkeiba.com/?pid=tool_group&group_id=110260"
r = session.get(pog_group_url)
r.raise_for_status()

# --- 4. HTML解析 ---
soup = BeautifulSoup(r.content, "html.parser")

# --- 5. メンバー名とポイント（賞金）をテーブルから抽出 ---
earnings = {}
rows = soup.select("table.list_table tbody tr")  # 正しいテーブルを指定

for row in rows:
    cols = row.find_all("td")
    if len(cols) >= 3:
        name_tag = cols[1].find("a")
        point_text = cols[2].get_text(strip=True).replace(",", "")
        if name_tag:
            member_name = name_tag.get_text(strip=True)
            try:
                point = float(point_text)
            except ValueError:
                point = 0.0
            earnings[member_name] = point

# --- 6. グループごとのポイント（賞金）を集計 ---
group_totals = {}
for group_name, members in GROUPS.items():
    total = sum(earnings.get(member, 0) for member in members)
    group_totals[group_name] = total


# --- 7. 結果を整形 ---
from datetime import datetime

# 現在日時取得＆フォーマット
now = datetime.now()
date_str = now.strftime("%m/%d 時点")

result_lines = [f"{date_str}【🏇 グループ別ポイントランキング】"]
for group, total in sorted(group_totals.items(), key=lambda x: x[1], reverse=True):
    result_lines.append(f"{group}: {total:,.0f} pt")
result_text = "\n".join(result_lines)

# --- 8. Discord通知 ---
if WEBHOOK_URL:
    requests.post(WEBHOOK_URL, json={"content": result_text})
    print("✅ Discordへ送信しました:\n", result_text)
else:
    print("⚠️ Webhook URLが未設定です。出力のみ行います：\n", result_text)
