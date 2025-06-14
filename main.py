#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EC自動化システム - メイン実行ファイル
"""

import asyncio
import argparse
import sys
from pathlib import Path

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent
sys.path.append(str(project_root))

def print_banner():
    """バナー表示"""
    banner = """
🚀 EC自動化システム - Amazon・楽天 × AI統合プラットフォーム
================================================================
    """
    print(banner)

def setup_environment():
    """環境セットアップ"""
    print("🔧 環境セットアップを開始します...")
    
    # .envファイルの存在確認
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if not env_file.exists() and env_example.exists():
        print("📝 .envファイルが見つからないため、.env.exampleからコピーします")
        try:
            import shutil
            shutil.copy(env_example, env_file)
            print("✅ .envファイルを作成しました")
            print("💡 .envファイルを編集して、実際のAPIキーを設定してください")
        except Exception as e:
            print(f"❌ .envファイル作成エラー: {e}")
    
    # 必要なディレクトリ作成
    directories = ["data", "logs", "results", "tests/results", "src/dashboard", "docs"]
    for dir_path in directories:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
    
    print("✅ 環境セットアップ完了")

def show_status():
    """システム状況表示"""
    try:
        from config.settings import get_config
        config = get_config()
        
        print("\n📊 システム状況:")
        print("-" * 40)
        print(f"デバッグモード: {config.debug_mode}")
        print(f"Gemini API: {'✅ 設定済み' if config.gemini_api_key else '❌ 未設定'}")
        print(f"Claude API: {'✅ 設定済み' if config.claude_api_key else '❌ 未設定'}")
        print(f"Amazon API: {'✅ 設定済み' if config.amazon_client_id else '❌ 未設定'}")
        print(f"楽天API: {'✅ 設定済み' if config.rakuten_service_secret else '❌ 未設定'}")
        
        # Notion設定確認
        import os
        notion_token = os.getenv('NOTION_TOKEN')
        notion_db_id = os.getenv('NOTION_DATABASE_ID')
        print(f"Notion API: {'✅ 設定済み' if notion_token else '❌ 未設定'}")
        print(f"NotionDB ID: {'✅ 設定済み' if notion_db_id else '❌ 未設定'}")
        
        # ダッシュボードファイル確認
        dashboard_files = [
            "src/dashboard/dashboard.html",
            "src/dashboard/dashboard_realtime.html"
        ]
        print(f"\nダッシュボード:")
        for file in dashboard_files:
            exists = Path(file).exists()
            print(f"  {file}: {'✅ 利用可能' if exists else '❌ 未作成'}")
            
    except Exception as e:
        print(f"❌ 設定読み込みエラー: {e}")
        print("💡 まず 'python main.py setup' を実行してください")

async def run_integration_test():
    """統合テスト実行"""
    try:
        from tests.integration_test import ECSystemIntegrationTest
        test_system = ECSystemIntegrationTest()
        results = await test_system.run_all_tests()
        test_system.print_recommendations()
        test_system.save_test_results()
        return results
    except Exception as e:
        print(f"❌ 統合テストエラー: {e}")
        return None

async def run_ai_analysis():
    """AI分析実行"""
    try:
        from src.ai_integration.ai_engine import ECAIIntegrationEngine
        engine = ECAIIntegrationEngine()
        results = await engine.run_integration_test()
        engine.save_results(results)
        return results
    except Exception as e:
        print(f"❌ AI分析エラー: {e}")
        return None

async def run_notion_sync():
    """Notion同期実行"""
    try:
        from src.notion_enhanced_integration import NotionECIntegration
        notion = NotionECIntegration()
        
        # 設定検証
        if not notion.validate_notion_config():
            print("❌ Notion設定が不完全です")
            print("💡 docs/NOTION_SETUP_GUIDE.md を参照してセットアップしてください")
            return False
        
        # 日次レポート同期
        print("📊 Notion日次レポートを同期中...")
        success = await notion.sync_daily_report()
        
        if success:
            print("🎉 Notion同期完了！")
            print("💡 Notionワークスペースで確認してください")
        else:
            print("❌ Notion同期に失敗しました")
        
        return success
        
    except Exception as e:
        print(f"❌ Notion同期エラー: {e}")
        return False

def generate_dashboard_data():
    """ダッシュボード用データ生成"""
    try:
        from src.automation_engine_24h import fetch_dashboard_data
        print("📊 ダッシュボードデータを生成中...")
        data = fetch_dashboard_data()
        print("✅ ダッシュボードデータ生成完了")
        return data
    except Exception as e:
        print(f"⚠️ ダッシュボードデータ生成エラー: {e}")
        print("💡 デモデータでダッシュボードを表示します")
        return None

def run_dashboard(realtime=False):
    """ダッシュボード起動"""
    import webbrowser
    import http.server
    import socketserver
    import threading
    
    # ダッシュボードファイル選択
    dashboard_file = "dashboard_realtime.html" if realtime else "dashboard.html"
    dashboard_path = Path(f"src/dashboard/{dashboard_file}")
    
    if not dashboard_path.exists():
        print(f"❌ ダッシュボードファイルが見つかりません: {dashboard_path}")
        print("💡 システムが完全にセットアップされていない可能性があります")
        return
    
    # ダッシュボードデータ生成（リアルタイム版の場合のみ）
    if realtime:
        generate_dashboard_data()
    
    # 簡易HTTPサーバー起動
    PORT = 8080
    
    class CustomHandler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(project_root), **kwargs)
    
    try:
        with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
            dashboard_type = "リアルタイム" if realtime else "標準"
            print(f"🌐 {dashboard_type}ダッシュボードサーバー起動中: http://localhost:{PORT}")
            
            # ブラウザでダッシュボードを開く
            dashboard_url = f"http://localhost:{PORT}/src/dashboard/{dashboard_file}"
            
            def open_browser():
                import time
                time.sleep(1)  # サーバー起動待ち
                webbrowser.open(dashboard_url)
            
            # ブラウザを別スレッドで開く
            browser_thread = threading.Thread(target=open_browser)
            browser_thread.daemon = True
            browser_thread.start()
            
            print(f"📊 ダッシュボードURL: {dashboard_url}")
            print("🛑 終了するには Ctrl+C を押してください")
            
            # サーバー実行
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n🛑 ダッシュボードサーバーを停止しました")
    except Exception as e:
        print(f"❌ サーバー起動エラー: {e}")

def run_automation_engine():
    """24時間自動化エンジン実行"""
    try:
        print("🤖 24時間自動化エンジンを開始します...")
        
        # データ生成
        data = generate_dashboard_data()
        
        if data:
            print("✅ 自動化エンジン実行完了")
            print(f"📊 売上データ: 今日¥{data['sales']['today']:,} / 週間¥{data['sales']['week_total']:,}")
            print(f"📦 在庫状況: {data['inventory']['total_items']}商品中 {data['inventory']['low_stock']}商品が要補充")
            print(f"💰 利益率: {data['profit']['profit_rate']:.1%}")
        
        return data
        
    except Exception as e:
        print(f"❌ 自動化エンジンエラー: {e}")
        return None

async def main():
    """メイン関数"""
    parser = argparse.ArgumentParser(
        description="EC自動化システム - Amazon・楽天 × AI統合プラットフォーム"
    )
    
    parser.add_argument(
        "command",
        choices=["test", "ai", "dashboard", "setup", "status", "automation", "realtime", "notion"],
        help="実行するコマンド"
    )
    
    parser.add_argument(
        "--debug",
        action="store_true",
        help="デバッグモードで実行"
    )
    
    args = parser.parse_args()
    
    # バナー表示
    print_banner()
    
    try:
        if args.command == "setup":
            setup_environment()
            
        elif args.command == "status":
            show_status()
            
        elif args.command == "test":
            print("🧪 統合テストを実行します...")
            results = await run_integration_test()
            
            if results and results["overall_status"] in ["excellent", "good"]:
                print("\n🎉 システムは正常に動作しています！")
            else:
                print("\n⚠️ システムに問題があります。設定を確認してください。")
                
        elif args.command == "ai":
            print("🤖 AI分析を実行します...")
            results = await run_ai_analysis()
            
            if results:
                print("\n🎉 AI分析が完了しました！")
            else:
                print("\n❌ AI分析でエラーが発生しました。")
                
        elif args.command == "notion":
            print("📊 Notion同期を実行します...")
            success = await run_notion_sync()
            
            if success:
                print("\n🎉 Notion同期が完了しました！")
                print("💡 Notionワークスペースでデータを確認してください")
            else:
                print("\n❌ Notion同期でエラーが発生しました。")
                
        elif args.command == "dashboard":
            print("📊 標準ダッシュボードを起動します...")
            run_dashboard(realtime=False)
            
        elif args.command == "realtime":
            print("📊 リアルタイムダッシュボードを起動します...")
            run_dashboard(realtime=True)
            
        elif args.command == "automation":
            print("🤖 24時間自動化エンジンを実行します...")
            data = run_automation_engine()
            
            if data:
                print("\n🎉 自動化エンジン実行完了！")
                print("💡 'python main.py realtime' でリアルタイムダッシュボードを確認できます")
                print("💡 'python main.py notion' でNotionに同期できます")
            else:
                print("\n❌ 自動化エンジンでエラーが発生しました。")
            
    except KeyboardInterrupt:
        print("\n🛑 実行を中断しました")
    except Exception as e:
        print(f"\n❌ エラーが発生しました: {e}")
        if args.debug:
            import traceback
            traceback.print_exc()

def show_help():
    """使用方法表示"""
    help_text = """
🚀 EC自動化システム - 使用方法

基本コマンド:
  python main.py setup      # 初期セットアップ
  python main.py status     # システム状況確認
  python main.py test       # 統合テスト実行
  python main.py ai         # AI分析実行
  
ダッシュボード:
  python main.py dashboard  # 標準ダッシュボード起動
  python main.py realtime   # リアルタイムダッシュボード起動
  
自動化・連携:
  python main.py automation # 24時間自動化エンジン実行
  python main.py notion     # Notion日次レポート同期

オプション:
  --debug                   # デバッグモードで実行

例:
  python main.py setup                    # 初回セットアップ
  python main.py status                   # 現在の状況確認
  python main.py realtime                 # リアルタイムダッシュボード
  python main.py notion                   # Notion同期実行
  python main.py automation --debug       # デバッグモードで自動化実行
    """
    print(help_text)

if __name__ == "__main__":
    # 引数なしの場合はヘルプ表示
    if len(sys.argv) == 1:
        show_help()
    else:
        # 非同期実行
        asyncio.run(main())
