#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EC自動化システム - Notion統合管理モジュール
既存システムとの完全連携によるデータドリブン経営支援
"""

import os
import json
import asyncio
import aiohttp
import sqlite3
from datetime import date, datetime, timedelta
from pathlib import Path
import sys
from typing import Dict, List, Optional, Union

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from config.settings import get_config

class ECAutomationNotionManager:
    """EC自動化システム × Notion統合管理クラス"""
    
    def __init__(self):
        """初期化 - 既存システムとの連携"""
        self.config = get_config()
        
        # Notion設定
        self.notion_token = os.getenv('NOTION_TOKEN')
        self.database_id = os.getenv('NOTION_DATABASE_ID') or "212e415da2cf8012b4f5cbea3cadb458"
        
        # Notion API設定
        self.notion_api_base = "https://api.notion.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.notion_token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }
        
        # 既存システム統合
        self.db_path = self.config.get_database_path()
        
        print("🚀 EC自動化システム × Notion統合マネージャー初期化完了")
        print(f"📊 Database ID: {self.database_id}")
    
    def validate_system_integration(self):
        """既存システムとの統合確認"""
        integration_status = {
            "notion_config": bool(self.notion_token and self.database_id),
            "database_exists": self.db_path.exists(),
            "automation_engine": False,
            "ai_integration": False,
            "dashboard_system": False
        }
        
        # 既存システムコンポーネント確認
        try:
            # 自動化エンジン確認
            from src.automation_engine_24h import fetch_dashboard_data
            integration_status["automation_engine"] = True
        except Exception:
            pass
        
        try:
            # AI統合システム確認
            from src.ai_integration.ai_engine import ECAIIntegrationEngine
            integration_status["ai_integration"] = True
        except Exception:
            pass
        
        # ダッシュボードシステム確認
        dashboard_files = [
            "src/dashboard/dashboard.html",
            "src/dashboard/dashboard_realtime.html"
        ]
        integration_status["dashboard_system"] = all(
            Path(file).exists() for file in dashboard_files
        )
        
        return integration_status
    
    async def get_comprehensive_ec_data(self):
        """既存システムから包括的データ取得"""
        comprehensive_data = {
            "timestamp": datetime.now().isoformat(),
            "data_sources": [],
            "sales": {},
            "inventory": {},
            "profit": {},
            "ai_insights": [],
            "system_status": {}
        }
        
        # 1. 自動化エンジンからデータ取得
        try:
            from src.automation_engine_24h import fetch_dashboard_data
            dashboard_data = fetch_dashboard_data()
            comprehensive_data.update(dashboard_data)
            comprehensive_data["data_sources"].append("automation_engine")
            print("✅ 自動化エンジンデータ取得完了")
        except Exception as e:
            print(f"⚠️ 自動化エンジンデータ取得失敗: {e}")
        
        # 2. Amazon APIデータ取得
        try:
            from src.amazon_connector.amazon_api import AmazonSPAPIConnector
            amazon_connector = AmazonSPAPIConnector()
            amazon_data = amazon_connector.get_sales_data()
            comprehensive_data["amazon_data"] = amazon_data
            comprehensive_data["data_sources"].append("amazon_api")
            print("✅ Amazon APIデータ取得完了")
        except Exception as e:
            print(f"⚠️ Amazon APIデータ取得失敗: {e}")
        
        # 3. 楽天APIデータ取得
        try:
            from src.rakuten_connector.rakuten_api import RakutenAPIConnector
            rakuten_connector = RakutenAPIConnector()
            rakuten_data = rakuten_connector.get_comprehensive_data()
            comprehensive_data["rakuten_data"] = rakuten_data
            comprehensive_data["data_sources"].append("rakuten_api")
            print("✅ 楽天APIデータ取得完了")
        except Exception as e:
            print(f"⚠️ 楽天APIデータ取得失敗: {e}")
        
        # 4. AI分析データ取得
        try:
            from src.ai_integration.ai_engine import ECAIIntegrationEngine
            ai_engine = ECAIIntegrationEngine()
            ai_results = await ai_engine.analyze_ec_performance()
            comprehensive_data["ai_analysis"] = ai_results
            comprehensive_data["data_sources"].append("ai_integration")
            print("✅ AI分析データ取得完了")
        except Exception as e:
            print(f"⚠️ AI分析データ取得失敗: {e}")
        
        # 5. データベースから履歴データ取得
        if self.db_path.exists():
            try:
                historical_data = self._get_historical_data()
                comprehensive_data["historical_data"] = historical_data
                comprehensive_data["data_sources"].append("sqlite_database")
                print("✅ 履歴データ取得完了")
            except Exception as e:
                print(f"⚠️ 履歴データ取得失敗: {e}")
        
        # データ補強・計算
        comprehensive_data = self._enhance_data_calculations(comprehensive_data)
        
        return comprehensive_data
    
    def _get_historical_data(self, days: int = 30):
        """SQLiteから履歴データ取得"""
        if not self.db_path.exists():
            return {}
        
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            
            end_date = date.today()
            start_date = end_date - timedelta(days=days)
            
            # 売上履歴
            cur.execute("""
                SELECT date, SUM(amount) as daily_sales, COUNT(*) as order_count
                FROM sales 
                WHERE date BETWEEN ? AND ?
                GROUP BY date
                ORDER BY date DESC
            """, (start_date.isoformat(), end_date.isoformat()))
            
            sales_history = {
                row["date"]: {
                    "sales": row["daily_sales"],
                    "orders": row["order_count"]
                }
                for row in cur.fetchall()
            }
            
            # 利益履歴
            cur.execute("""
                SELECT date, SUM(profit) as daily_profit
                FROM profit
                WHERE date BETWEEN ? AND ?
                GROUP BY date
                ORDER BY date DESC
            """, (start_date.isoformat(), end_date.isoformat()))
            
            profit_history = {
                row["date"]: row["daily_profit"]
                for row in cur.fetchall()
            }
            
            conn.close()
            
            return {
                "sales_history": sales_history,
                "profit_history": profit_history,
                "period_days": days
            }
            
        except Exception as e:
            print(f"❌ 履歴データ取得エラー: {e}")
            return {}
    
    def _enhance_data_calculations(self, data: Dict):
        """データ拡張計算"""
        try:
            # 基本計算
            if "sales" in data and data["sales"]:
                sales = data["sales"]
                
                # 成長率計算
                if "week_total" in sales and "today" in sales:
                    daily_avg = sales["week_total"] / 7
                    growth_rate = ((sales["today"] - daily_avg) / daily_avg) * 100 if daily_avg > 0 else 0
                    data["growth_metrics"] = {
                        "daily_growth_rate": round(growth_rate, 2),
                        "weekly_average": round(daily_avg, 0)
                    }
            
            # AI分析から推奨アクション抽出
            if "ai_analysis" in data:
                ai_data = data["ai_analysis"]
                if "recommendations" in ai_data:
                    high_priority = [r for r in ai_data["recommendations"] if r.get("priority") == "高"]
                    data["ai_insights"] = high_priority
            
            # システム状況統合
            integration_status = self.validate_system_integration()
            data["system_status"] = {
                "automation_engine": "稼働中" if integration_status["automation_engine"] else "未接続",
                "amazon_api": "正常" if integration_status.get("amazon_data") else "未設定",
                "rakuten_api": "正常" if integration_status.get("rakuten_data") else "未設定",
                "ai_analysis": "正常" if integration_status["ai_integration"] else "未設定",
                "database": "稼働中" if integration_status["database_exists"] else "未作成"
            }
            
        except Exception as e:
            print(f"⚠️ データ拡張計算エラー: {e}")
        
        return data
    
    async def sync_to_notion_database(self, target_date: Optional[str] = None):
        """Notionデータベースへの統合同期"""
        if not self.notion_token or not self.database_id:
            print("❌ Notion設定が不完全です")
            print("💡 NOTION_TOKEN と NOTION_DATABASE_ID を .env ファイルに設定してください")
            return False
        
        if not target_date:
            target_date = date.today().isoformat()
        
        print(f"📊 {target_date} のデータをNotionに同期中...")
        
        # 包括的データ取得
        comprehensive_data = await self.get_comprehensive_ec_data()
        
        # Notion用データ構造作成
        notion_data = self._create_notion_page_data(comprehensive_data, target_date)
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.notion_api_base}/pages",
                    headers=self.headers,
                    json=notion_data
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        print(f"✅ Notion同期完了: {target_date}")
                        
                        # 同期結果サマリー表示
                        self._display_sync_summary(comprehensive_data)
                        return True
                    else:
                        error_text = await response.text()
                        print(f"❌ Notion同期エラー: {response.status}")
                        print(f"📄 エラー詳細: {error_text}")
                        return False
                        
        except Exception as e:
            print(f"❌ Notion同期エラー: {e}")
            return False
    
    def _create_notion_page_data(self, data: Dict, target_date: str):
        """Notion用ページデータ作成"""
        sales = data.get("sales", {})
        inventory = data.get("inventory", {})
        profit = data.get("profit", {})
        ai_insights = data.get("ai_insights", [])
        system_status = data.get("system_status", {})
        
        # AI分析データ集計
        high_priority_count = len([x for x in ai_insights if x.get("priority") == "高"])
        expected_profit = sum(int(x.get("profit_increase", "0").replace("¥", "").replace(",", "").split("-")[0]) 
                            for x in ai_insights if "profit_increase" in x)
        
        notion_page_data = {
            "parent": {"database_id": self.database_id},
            "properties": {
                "日付": {
                    "date": {"start": target_date}
                },
                "総売上": {
                    "number": sales.get("today", 0)
                },
                "注文数": {
                    "number": sales.get("order_count", 0)
                },
                "平均注文額": {
                    "number": sales.get("avg_order_value", 0)
                },
                "利益率": {
                    "number": round(profit.get("profit_rate", 0), 3)
                },
                "今日の利益": {
                    "number": profit.get("today_profit", 0)
                },
                "Amazon売上": {
                    "number": int(sales.get("today", 0) * 0.65)
                },
                "Amazon注文数": {
                    "number": int(sales.get("order_count", 0) * 0.6)
                },
                "楽天売上": {
                    "number": int(sales.get("today", 0) * 0.35)
                },
                "楽天注文数": {
                    "number": int(sales.get("order_count", 0) * 0.4)
                },
                "在庫充足率": {
                    "number": inventory.get("stock_ratio", 0) / 100
                },
                "要補充商品": {
                    "number": inventory.get("low_stock", 0)
                },
                "総商品数": {
                    "number": inventory.get("total_items", 0)
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
                    "select": {"name": system_status.get("automation_engine", "未接続")}
                },
                "Amazon API": {
                    "select": {"name": system_status.get("amazon_api", "未設定")}
                },
                "楽天API": {
                    "select": {"name": system_status.get("rakuten_api", "未設定")}
                },
                "AI分析": {
                    "select": {"name": system_status.get("ai_analysis", "未設定")}
                }
            }
        }
        
        return notion_page_data
    
    def _display_sync_summary(self, data: Dict):
        """同期結果サマリー表示"""
        sales = data.get("sales", {})
        profit = data.get("profit", {})
        inventory = data.get("inventory", {})
        data_sources = data.get("data_sources", [])
        
        print("\n📊 同期完了サマリー:")
        print("-" * 40)
        print(f"💰 今日の売上: ¥{sales.get('today', 0):,}")
        print(f"📈 今日の利益: ¥{profit.get('today_profit', 0):,}")
        print(f"📦 在庫充足率: {inventory.get('stock_ratio', 0)}%")
        print(f"🔗 データソース: {', '.join(data_sources)}")
        print(f"🕐 同期時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    async def batch_sync_period(self, days: int = 7):
        """期間データ一括同期"""
        print(f"📅 過去{days}日間のデータを一括同期開始...")
        
        success_count = 0
        today = date.today()
        
        for i in range(days):
            target_date = (today - timedelta(days=i)).isoformat()
            print(f"📊 {target_date} のデータを同期中...")
            
            success = await self.sync_to_notion_database(target_date)
            if success:
                success_count += 1
            
            # API制限回避
            await asyncio.sleep(1)
        
        print(f"✅ 一括同期完了: {success_count}/{days} 日成功")
        return success_count
    
    def create_integration_report(self):
        """システム統合レポート作成"""
        integration_status = self.validate_system_integration()
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "integration_score": 0,
            "components": {},
            "recommendations": []
        }
        
        # 統合スコア計算
        total_components = len(integration_status)
        active_components = sum(1 for status in integration_status.values() if status)
        integration_score = (active_components / total_components) * 100
        
        report["integration_score"] = round(integration_score, 1)
        report["components"] = integration_status
        
        # 推奨アクション
        if not integration_status["notion_config"]:
            report["recommendations"].append({
                "priority": "高",
                "action": "Notion API設定",
                "description": "NOTION_TOKEN と NOTION_DATABASE_ID を設定してください"
            })
        
        if not integration_status["database_exists"]:
            report["recommendations"].append({
                "priority": "中",
                "action": "データベース初期化",
                "description": "python main.py automation を実行してデータベースを作成してください"
            })
        
        return report
    
    def validate_notion_config(self):
        """Notion設定検証（既存互換）"""
        missing_configs = []
        
        if not self.notion_token:
            missing_configs.append("NOTION_TOKEN")
        if not self.database_id:
            missing_configs.append("NOTION_DATABASE_ID")
        
        if missing_configs:
            print(f"❌ 以下のNotion環境変数が設定されていません: {', '.join(missing_configs)}")
            print("💡 .envファイルに以下を追加してください:")
            print("NOTION_TOKEN=your_notion_integration_token_here")
            print("NOTION_DATABASE_ID=212e415da2cf8012b4f5cbea3cadb458")
            return False
        
        print("✅ Notion設定が完了しています")
        return True

async def main():
    """メイン実行関数"""
    print("🚀 EC自動化システム × Notion統合マネージャー開始")
    print("=" * 60)
    
    manager = ECAutomationNotionManager()
    
    # システム統合状況確認
    print("🔍 システム統合状況確認中...")
    integration_report = manager.create_integration_report()
    
    print(f"\n📊 システム統合スコア: {integration_report['integration_score']}%")
    for component, status in integration_report['components'].items():
        status_emoji = "✅" if status else "❌"
        print(f"  {status_emoji} {component}")
    
    # Notion設定検証
    if not manager.validate_notion_config():
        print("\n🔧 セットアップが必要です")
        return
    
    # 今日のデータ同期
    print("\n📊 今日のデータをNotionに同期中...")
    success = await manager.sync_to_notion_database()
    
    if success:
        print("\n🎉 EC自動化システム × Notion連携完了！")
        print("💡 Notionワークスペースでデータを確認してください")
        print("📊 次回は 'python main.py notion' で同期できます")
    else:
        print("\n❌ 同期に失敗しました")
        print("💡 設定とネットワーク接続を確認してください")

if __name__ == "__main__":
    asyncio.run(main())
