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
    directories = ["data", "logs", "results", "tests/results"]
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

def run_dashboard():
    """ダッシュボード起動"""
    import webbrowser
    import http.server
    import socketserver
    import threading
    
    # ダッシュボードファイルパス
    dashboard_path = Path("src/dashboard/dashboard.html")
    
    if not dashboard_path.exists():
        print("❌ ダッシュボードファイルが見つかりません")
        print("💡 システムが完全にセットアップされていない可能性があります")
        return
    
    # 簡易HTTPサーバー起動
    PORT = 8080
    
    class CustomHandler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(project_root), **kwargs)
    
    try:
        with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
            print(f"🌐 ダッシュボードサーバー起動中: http://localhost:{PORT}")
            
            # ブラウザでダッシュボードを開く
            dashboard_url = f"http://localhost:{PORT}/src/dashboard/dashboard.html"
            
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

async def main():
    """メイン関数"""
    parser = argparse.ArgumentParser(
        description="EC自動化システム - Amazon・楽天 × AI統合プラットフォーム"
    )
    
    parser.add_argument(
        "command",
        choices=["test", "ai", "dashboard", "setup", "status"],
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
                
        elif args.command == "dashboard":
            print("📊 ダッシュボードを起動します...")
            run_dashboard()
            
    except KeyboardInterrupt:
        print("\n🛑 実行を中断しました")
    except Exception as e:
        print(f"\n❌ エラーが発生しました: {e}")
        if args.debug:
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    # 非同期実行
    asyncio.run(main())
