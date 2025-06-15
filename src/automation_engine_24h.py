#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""24時間自動化エンジン - ダッシュボード用データ生成スクリプト"""

import sqlite3
import json
from datetime import date, timedelta, datetime
from pathlib import Path
import sys
import os
from notion_client import Client

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from config.settings import get_config


def fetch_dashboard_data():
    """SQLiteデータベースから売上・在庫・利益情報を取得しJSON出力"""
    config = get_config()
    db_path = config.get_database_path()

    if not db_path.exists():
        raise FileNotFoundError(f"データベースが見つかりません: {db_path}")

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    today = date.today()
    start_date = today - timedelta(days=6)

    def fetch_one(query: str, params=()):
        cur.execute(query, params)
        row = cur.fetchone()
        return row[0] if row and row[0] is not None else 0

    # 売上データ
    today_sales = fetch_one(
        "SELECT SUM(amount) FROM sales WHERE date = ?",
        (today.isoformat(),),
    )
    week_sales = fetch_one(
        "SELECT SUM(amount) FROM sales WHERE date BETWEEN ? AND ?",
        (start_date.isoformat(), today.isoformat()),
    )
    order_count = fetch_one(
        "SELECT COUNT(*) FROM sales WHERE date BETWEEN ? AND ?",
        (start_date.isoformat(), today.isoformat()),
    )
    avg_order = int(week_sales / order_count) if order_count else 0

    cur.execute(
        "SELECT date, SUM(amount) AS total FROM sales WHERE date BETWEEN ? AND ? "
        "GROUP BY date ORDER BY date",
        (start_date.isoformat(), today.isoformat()),
    )
    daily_sales = {row["date"]: row["total"] for row in cur.fetchall()}

    # 在庫データ
    total_items = fetch_one("SELECT COUNT(*) FROM inventory")
    low_stock = fetch_one(
        "SELECT COUNT(*) FROM inventory WHERE stock <= reorder_level"
    )
    stock_ratio = fetch_one(
        "SELECT AVG(stock_ratio) FROM (SELECT stock * 1.0 / CASE WHEN capacity = 0 THEN NULL ELSE capacity END AS stock_ratio FROM inventory)"
    )

    # 利益データ
    today_profit = fetch_one(
        "SELECT SUM(profit) FROM profit WHERE date = ?",
        (today.isoformat(),),
    )
    week_profit = fetch_one(
        "SELECT SUM(profit) FROM profit WHERE date BETWEEN ? AND ?",
        (start_date.isoformat(), today.isoformat()),
    )
    profit_rate = (week_profit / week_sales) if week_sales else 0

    conn.close()

    data = {
        "sales": {
            "today": today_sales,
            "week_total": week_sales,
            "order_count": order_count,
            "avg_order_value": avg_order,
            "daily_sales": daily_sales,
        },
        "inventory": {
            "stock_ratio": round(stock_ratio * 100, 1) if stock_ratio else 0,
            "low_stock": low_stock,
            "total_items": total_items,
        },
        "profit": {
            "today_profit": today_profit,
            "week_profit": week_profit,
            "profit_rate": round(profit_rate, 3),
        },
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    output_path = Path("src/dashboard/dashboard_data.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"✅ Dashboard data updated: {output_path}")

    # Notion同期
    NOTION_TOKEN = "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"
    NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

    if NOTION_DATABASE_ID:
        try:
            notion = Client(auth=NOTION_TOKEN)
            notion.pages.create(
                parent={"database_id": NOTION_DATABASE_ID},
                properties={
                    "日付": {"date": {"start": datetime.now().date().isoformat()}},
                    "売上": {"number": data["sales"]["today"]},
                    "在庫率": {"number": data["inventory"]["stock_ratio"]},
                    "利益": {"number": data["profit"]["today_profit"]},
                    "利益率": {"number": data["profit"]["profit_rate"]},
                },
            )
            print("✅ Notionへ投稿しました")
        except Exception as e:
            print(f"❌ Notion投稿エラー: {e}")
    else:
        print("ℹ️ NOTION_DATABASE_ID が設定されていないため Notion への投稿をスキップします")

    return data


if __name__ == "__main__":
    fetch_dashboard_data()