{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyOkSKOCQixxiyzbdTxJAt7T",
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/tachyon0133-oss/my-first-repo/blob/main/rank.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "import os\n",
        "import requests\n",
        "from bs4 import BeautifulSoup\n",
        "\n",
        "# --- 1. グループ分け定義 ---\n",
        "GROUPS = {\n",
        "    \"グループ①\": [\"みくろん\", \"うた\", \"えろっぴ\", \"あさの\"],\n",
        "    \"グループ②\": [\"9292\", \"大村\", \"bago\", \"アンクラ\"],\n",
        "    \"グループ③\": [\"gonbeyy\", \"kaomoji\", \"なしょ\", \"ばーす\"]\n",
        "}\n",
        "\n",
        "# --- 2. Discord Webhook（環境変数から取得推奨） ---\n",
        "WEBHOOK_URL = WEBHOOK_URL = \"https://discord.com/api/webhooks/1381637611898277979/HEx1SeofnZrpMakiNjrAZ5f4CAYdJybb28u7iUVWqyk_jslchh6VJj56im0KD8I_qVkB\"\n",
        "\n",
        "# --- 3. セッションとページ取得（ログインなし前提） ---\n",
        "session = requests.Session()\n",
        "pog_group_url = \"https://pog.netkeiba.com/?pid=tool_group&group_id=110260\"\n",
        "r = session.get(pog_group_url)\n",
        "r.raise_for_status()\n",
        "\n",
        "# --- 4. HTML解析 ---\n",
        "soup = BeautifulSoup(r.content, \"html.parser\")\n",
        "\n",
        "# --- 5. メンバー名とポイント（賞金）をテーブルから抽出 ---\n",
        "earnings = {}\n",
        "rows = soup.select(\"table.list_table tbody tr\")  # 正しいテーブルを指定\n",
        "\n",
        "for row in rows:\n",
        "    cols = row.find_all(\"td\")\n",
        "    if len(cols) >= 3:\n",
        "        name_tag = cols[1].find(\"a\")\n",
        "        point_text = cols[2].get_text(strip=True).replace(\",\", \"\")\n",
        "        if name_tag:\n",
        "            member_name = name_tag.get_text(strip=True)\n",
        "            try:\n",
        "                point = float(point_text)\n",
        "            except ValueError:\n",
        "                point = 0.0\n",
        "            earnings[member_name] = point\n",
        "\n",
        "# --- 6. グループごとのポイント（賞金）を集計 ---\n",
        "group_totals = {}\n",
        "for group_name, members in GROUPS.items():\n",
        "    total = sum(earnings.get(member, 0) for member in members)\n",
        "    group_totals[group_name] = total\n",
        "\n",
        "\n",
        "# --- 7. 結果を整形 ---\n",
        "from datetime import datetime\n",
        "\n",
        "# 現在日時取得＆フォーマット\n",
        "now = datetime.now()\n",
        "date_str = now.strftime(\"%m/%d 時点\")\n",
        "\n",
        "result_lines = [f\"{date_str}【🏇 グループ別ポイントランキング】\"]\n",
        "for group, total in sorted(group_totals.items(), key=lambda x: x[1], reverse=True):\n",
        "    result_lines.append(f\"{group}: {total:,.0f} pt\")\n",
        "result_text = \"\\n\".join(result_lines)\n",
        "\n",
        "# --- 8. Discord通知 ---\n",
        "if WEBHOOK_URL:\n",
        "    requests.post(WEBHOOK_URL, json={\"content\": result_text})\n",
        "    print(\"✅ Discordへ送信しました:\\n\", result_text)\n",
        "else:\n",
        "    print(\"⚠️ Webhook URLが未設定です。出力のみ行います：\\n\", result_text)\n"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "bIWBTndBsRYg",
        "outputId": "e92e9eac-5e22-4f3f-d940-ea253d6fb9f5"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "✅ Discordへ送信しました:\n",
            " 08/12 時点【🏇 グループ別ポイントランキング】\n",
            "グループ③: 8,540 pt\n",
            "グループ①: 5,460 pt\n",
            "グループ②: 4,424 pt\n"
          ]
        }
      ]
    }
  ]
}