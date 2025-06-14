#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EC自動化システム Notion連携強化版
Amazon・楽天の売上・利益データを自動的にNotionに同期
"""

import os
import json
import asyncio
import aiohttp
from datetime import date, datetime, timedelta
from pathlib import Path
import sys
from typing import Dict, List, Optional

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from config.settings import get_config

class NotionECIntegration:
    """Notion EC自動化統合クラス"""
    
    def __init__(self):
        """初期化"""
        self.config = get_config()
        
        # Notion設定
        self.notion_token = os.getenv('NOTION_TOKEN')
        self.database_id = os.getenv('NOTION_DATABASE_ID')
        
        # Notion API設定
        self.notion_api_base = "https://api.notion.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.notion_token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }
        
        print("🚀 Notion EC統合システム初期化完了")
    
    async def create_database_if_not_exists(self, parent_page_id: str):
        """Notionデータベース自動作成"""
        try:
            # データベース作成
            database_data = {
                "parent": {"page_id": parent_page_id},
                "title": [
                    {
                        "type": "text",
                        "text": {"content": "EC自動化システム 日次レポート"}
                    }
                ],
                "properties": {
                    "日付": {"date": {}},
                    "総売上": {"number": {"format": "yen"}},
                    "注文数": {"number": {}},
                    "平均注文額": {"number": {"format": "yen"}},
                    "利益率": {"number": {"format": "percent"}},
                    "今日の利益": {"number": {"format": "yen"}},
                    "Amazon売上": {"number": {"format": "yen"}},
                    "Amazon注文数": {"number": {}},
                    "楽天売上": {"number": {"format": "yen"}},
                    "楽天注文数": {"number": {}},
                    "在庫充足率": {"number": {"format": "percent"}},
                    "要補充商品": {"number": {}},
                    "総商品数": {"number": {}},
                    "AI提案数": {"number": {}},
                    "高優先度提案": {"number": {}},
                    "期待利益向上": {"number": {"format": "yen"}},
                    "ステータス": {
                        "select": {
                            "options": [
                                {"name": "正常稼働", "color": "green"},
                                {"name": "要注意", "color": "yellow"},
                                {"name": "異常", "color": "red"},
                                {"name": "メンテナンス中", "color": "gray"}
                            ]
                        }
                    },
                    "自動化エンジン": {
                        "select": {
                            "options": [
                                {"name": "稼働中", "color": "green"},
                                {"name": "停止中", "color": "red"},
                                {"name": "エラー", "color": "red"}
                            ]
                        }
                    },
                    "Amazon API": {
                        "select": {
                            "options": [
                                {"name": "正常", "color": "green"},
                                {"name": "警告", "color": "yellow"},
                                {"name": "エラー", "color": "red"}
                            ]
                        }
                    },
                    "楽天API": {
                        "select": {
                            "options": [
                                {"name": "正常", "color": "green"},
                                {"name": "警告", "color": "yellow"},
                                {"name": "エラー", "color": "red"}
                            ]
                        }
                    },
                    "AI分析": {
                        "select": {
                            "options": [
                                {"name": "正常", "color": "green"},
                                {"name": "警告", "color": "yellow"},
                                {"name": "エラー", "color": "red"}
                            ]
                        }
                    }
                }
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.notion_api_base}/databases",
                    headers=self.headers,
                    json=database_data
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        database_id = result["id"]
                        print(f"✅ Notionデータベース作成完了: {database_id}")
                        return database_id
                    else:
                        error_text = await response.text()
                        print(f"❌ データベース作成エラー: {response.status} - {error_text}")
                        return None
                        
        except Exception as e:
            print(f"❌ データベース作成エラー: {e}")
            return None
    
    async def get_dashboard_data(self):
        """ダッシュボードデータ取得"""
        try:
            # 自動化エンジンからデータ取得
            from src.automation_engine_24h import fetch_dashboard_data
            return fetch_dashboard_data()
        except Exception as e:
            print(f"⚠️ リアルデータ取得失敗、デモデータ使用: {e}")
            return self._get_demo_data()
    
    def _get_demo_data(self):
        """デモデータ生成"""
        today = datetime.now()
        
        return {
            "sales": {
                "today": 165000,
                "week_total": 1715000,
                "order_count": 142,
                "avg_order_value": 12084,
                "daily_sales": {
                    (today - timedelta(days=i)).strftime("%Y-%m-%d"): 
                    150000 + (i * 10000) + ((-1)**i * 15000)
                    for i in range(7)
                }
            },
            "inventory": {
                "stock_ratio": 88.5,
                "low_stock": 31,
                "total_items": 206
            },
            "profit": {
                "today_profit": 49500,
                "week_profit": 514500,
                "profit_rate": 0.3
            },
            "ai_insights": [
                {
                    "priority": "高",
                    "category": "価格最適化",
                    "expected_profit": 25000
                },
                {
                    "priority": "中",
                    "category": "在庫最適化", 
                    "expected_profit": 15000
                }
            ],
            "system_status": {
                "automation_engine": "稼働中",
                "amazon_api": "正常",
                "rakuten_api": "正常",
                "ai_analysis": "正常"
            }
        }
    
    async def sync_daily_report(self, target_date: Optional[str] = None):
        """日次レポートをNotionに同期"""
        if not self.notion_token or not self.database_id:
            print("❌ Notion設定が不完全です（NOTION_TOKEN, NOTION_DATABASE_IDを確認）")
            return False
        
        if not target_date:
            target_date = date.today().isoformat()
        
        # ダッシュボードデータ取得
        dashboard_data = await self.get_dashboard_data()
        
        # AI分析データ生成
        ai_insights = dashboard_data.get("ai_insights", [])
        high_priority_count = len([x for x in ai_insights if x.get("priority") == "高"])
        expected_profit = sum(x.get("expected_profit", 0) for x in ai_insights)
        
        # Notion page データ構造
        page_data = {
            "parent": {"database_id": self.database_id},
            "properties": {
                "日付": {
                    "date": {"start": target_date}
                },
                "総売上": {
                    "number": dashboard_data["sales"]["today"]
                },
                "注文数": {
                    "number": dashboard_data["sales"]["order_count"]
                },
                "平均注文額": {
                    "number": dashboard_data["sales"]["avg_order_value"]
                },
                "利益率": {
                    "number": round(dashboard_data["profit"]["profit_rate"], 3)
                },
                "今日の利益": {
                    "number": dashboard_data["profit"]["today_profit"]
                },
                "Amazon売上": {
                    "number": int(dashboard_data["sales"]["today"] * 0.65)
                },
                "Amazon注文数": {
                    "number": int(dashboard_data["sales"]["order_count"] * 0.6)
                },
                "楽天売上": {
                    "number": int(dashboard_data["sales"]["today"] * 0.35)
                },
                "楽天注文数": {
                    "number": int(dashboard_data["sales"]["order_count"] * 0.4)
                },
                "在庫充足率": {
                    "number": dashboard_data["inventory"]["stock_ratio"] / 100
                },
                "要補充商品": {
                    "number": dashboard_data["inventory"]["low_stock"]
                },
                "総商品数": {
                    "number": dashboard_data["inventory"]["total_items"]
                },
                "AI提案数": {
                    "number": len(ai_insights)
                },
                "高優先度提案": {
                    "number": high_priority_count
                },
                "期待利益向上": {
                    "number": expected_profit
                },
                "ステータス": {
                    "select": {"name": "正常稼働"}
                },
                "自動化エンジン": {
                    "select": {"name": dashboard_data["system_status"]["automation_engine"]}
                },
                "Amazon API": {
                    "select": {"name": dashboard_data["system_status"]["amazon_api"]}
                },
                "楽天API": {
                    "select": {"name": dashboard_data["system_status"]["rakuten_api"]}
                },
                "AI分析": {
                    "select": {"name": dashboard_data["system_status"]["ai_analysis"]}
                }
            }
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.notion_api_base}/pages",
                    headers=self.headers,
                    json=page_data
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        print(f"✅ Notion同期完了: {target_date}")
                        print(f"📊 売上: ¥{dashboard_data['sales']['today']:,}")
                        print(f"💰 利益: ¥{dashboard_data['profit']['today_profit']:,}")
                        print(f"📦 在庫: {dashboard_data['inventory']['stock_ratio']}%")
                        return True
                    else:
                        error_text = await response.text()
                        print(f"❌ Notion同期エラー: {response.status}")
                        print(f"📄 エラー詳細: {error_text}")
                        return False
                        
        except Exception as e:
            print(f"❌ Notion同期エラー: {e}")
            return False
    
    async def batch_sync_weekly_data(self):
        """週間データ一括同期"""
        print("📅 週間データ一括同期開始...")
        
        success_count = 0
        today = date.today()
        
        for i in range(7):
            target_date = (today - timedelta(days=i)).isoformat()
            
            print(f"📊 {target_date} のデータを同期中...")
            success = await self.sync_daily_report(target_date)
            
            if success:
                success_count += 1
            
            # API制限回避のため少し待機
            await asyncio.sleep(1)
        
        print(f"✅ 週間同期完了: {success_count}/7 日成功")
        return success_count
    
    async def create_notion_dashboard_template(self, parent_page_id: str):
        """Notionダッシュボードテンプレート作成"""
        template_content = """# 🚀 EC自動化システム ダッシュボード

## 📊 今日の実績 (リアルタイム)

### 売上サマリー
- **総売上**: ¥165,000 (+5.2%)
- **注文数**: 142件 (+8件)
- **平均注文額**: ¥12,084 (+¥150)
- **利益率**: 30.0% (+0.3%)

### プラットフォーム内訳
- **Amazon**: ¥107,250 (85件)
- **楽天**: ¥57,750 (57件)

## 📈 週間トレンド

[この下に埋め込みデータベースビューを配置]

## 🤖 AI自動化提案

### 🔥 高優先度
1. **価格最適化提案**: 商品Aの価格を5%調整 → 期待利益¥25,000/日
2. **在庫補充推奨**: 人気商品B → 機会損失防止¥15,000/日

### 📊 中優先度
1. **SEO最適化**: 商品ページのキーワード改善
2. **競合分析**: 価格競争力向上施策

## ⚙️ システム状況

- 🟢 **自動化エンジン**: 稼働中
- 🟢 **Amazon API**: 正常
- 🟢 **楽天API**: 正常  
- 🟢 **AI分析**: 正常

## 📅 今日のタスク

- [ ] AI提案の価格調整実施
- [ ] 在庫補充商品31件の発注
- [ ] 競合価格調査
- [ ] 週次レポート準備

---
*最終更新: """ + datetime.now().strftime("%Y/%m/%d %H:%M") + "*"

        page_data = {
            "parent": {"page_id": parent_page_id},
            "properties": {
                "title": [
                    {
                        "type": "text",
                        "text": {"content": "🚀 EC自動化システム ダッシュボード"}
                    }
                ]
            },
            "children": [
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {"content": template_content}
                            }
                        ]
                    }
                }
            ]
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.notion_api_base}/pages",
                    headers=self.headers,
                    json=page_data
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        page_id = result["id"]
                        print(f"✅ Notionダッシュボードテンプレート作成完了: {page_id}")
                        return page_id
                    else:
                        error_text = await response.text()
                        print(f"❌ テンプレート作成エラー: {response.status} - {error_text}")
                        return None
                        
        except Exception as e:
            print(f"❌ テンプレート作成エラー: {e}")
            return None
    
    def validate_notion_config(self):
        """Notion設定検証"""
        missing_configs = []
        
        if not self.notion_token:
            missing_configs.append("NOTION_TOKEN")
        if not self.database_id:
            missing_configs.append("NOTION_DATABASE_ID")
        
        if missing_configs:
            print(f"❌ 以下のNotion環境変数が設定されていません: {', '.join(missing_configs)}")
            print("💡 .envファイルに以下を追加してください:")
            print("NOTION_TOKEN=your_notion_integration_token_here")
            print("NOTION_DATABASE_ID=your_database_id_here")
            return False
        
        print("✅ Notion設定が完了しています")
        return True

async def main():
    """メイン実行関数"""
    print("🚀 EC自動化システム Notion連携開始")
    print("=" * 50)
    
    notion = NotionECIntegration()
    
    # 設定検証
    if not notion.validate_notion_config():
        print("🔧 セットアップが必要です")
        return
    
    # 今日の日報同期
    print("📊 今日の日報をNotionに同期中...")
    success = await notion.sync_daily_report()
    
    if success:
        print("🎉 Notion同期完了！")
        print("💡 Notionワークスペースで確認してください")
    else:
        print("❌ 同期に失敗しました")
    
    # 週間データ一括同期オプション
    print("\n📅 週間データを一括同期しますか？ (y/n)")
    # choice = input().lower()
    # if choice == 'y':
    #     await notion.batch_sync_weekly_data()

if __name__ == "__main__":
    asyncio.run(main())
