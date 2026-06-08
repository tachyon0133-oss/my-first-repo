import os
import requests
from bs4 import BeautifulSoup

# --- 1. グループ分け定義 ---
GROUPS = {
    "グループ①": ["ごんべい", "アンクラ", "えろっぴ", "かずーい"],
    "グループ②": ["9292", "あさの", "bago", "kaomoji"],
    "グループ③": ["うた", "みくろん", "なしょ", "ばーす"]
}

TEAMS = {
    "グループ１": ["グループ１"],
    "グループ２": ["グループ２"],
    "グループ３": ["グループ３"]
}

# --- 2. Discord Webhook（環境変数から取得推奨） ---
WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

# --- 3. セッションとページ取得（ログインなし前提） ---
session = requests.Session()
pog_group_url = "https://pog.netkeiba.com/?pid=tool_group&group_id=117946"
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

# --- 5-1. グループ枠とポイント（賞金）をテーブルから抽出 ---
earnings_gr = {}
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
            earnings_gr[member_name] = point
            
# --- 6. グループごとのポイント（賞金）を集計 ---
group_totals = {}
for group_name, members in GROUPS.items():
    total = sum(earnings.get(member, 0) for member in members)
    group_totals[group_name] = total
            
# --- 6-1. グループ枠ごとのポイント（賞金）を集計 ---
groups_totals = {}
for group_name, members in TEAMS.items():
    total = sum(earnings_gr.get(member, 0) for member in members)
    groups_totals[group_name] = total
    
# --- 7. 結果を整形 ---
from datetime import datetime

# 現在日時取得＆フォーマット
now = datetime.now()
date_str = now.strftime("%m/%d 時点")

result_lines = [f"{date_str}\n【🏇 グループ別ポイントランキング】"]
for group, total in sorted(group_totals.items(), key=lambda x: x[1], reverse=True):
    result_lines.append(f"{group}: {total:,.0f} pt")
result_text = "\n".join(result_lines)

# グループ枠
result_gr_lines = [f"\n【🐶 グループ枠ポイントランキング】"]
for group, total in sorted(groups_totals.items(), key=lambda x: x[1], reverse=True):
    result_gr_lines.append(f"{group}: {total:,.0f} pt")
result_gr_text = result_text + "\n" + "\n".join(result_gr_lines)


# --- 8. Discord通知 ---
if WEBHOOK_URL:
    requests.post(WEBHOOK_URL, json={"content": result_gr_text})
    print("✅ Discordへ送信しました:\n", result_gr_text)
else:
    print("⚠️ Webhook URLが未設定です。出力のみ行います：\n", result_gr_text)
