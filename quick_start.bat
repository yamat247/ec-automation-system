@echo off
REM 🚀 EC自動化システム - Windows クイックスタート
REM 使用方法: quick_start.bat をダブルクリック

echo 🚀 EC自動化システム - Windows クイックスタート開始
echo ==================================================

REM 1. 現在のディレクトリ確認
echo 📍 現在のディレクトリ: %CD%

REM 2. Python環境確認
echo 🐍 Python環境確認...
python --version
if errorlevel 1 (
    echo ❌ Python がインストールされていません
    echo 📥 https://python.org からPython 3.8以上をインストールしてください
    pause
    exit /b 1
)

REM 3. 依存関係インストール
echo 📦 依存関係インストール中...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ 依存関係のインストールに失敗しました
    pause
    exit /b 1
)

REM 4. .envファイル作成
echo ⚙️ 環境変数ファイル準備中...
if not exist .env (
    copy .env.example .env
    echo ✅ .envファイルを作成しました
    echo.
    echo 🔑 重要: 次に .env ファイルを編集してAPIキーを設定してください
    echo 📝 .envファイルをメモ帳で開きます...
    timeout /t 3 /nobreak >nul
    notepad .env
    echo.
    echo 必要なAPIキー:
    echo - GEMINI_API_KEY: Google AI Studio で取得
    echo - CLAUDE_API_KEY: Anthropic Console で取得
    echo - AMAZON_CLIENT_ID: Amazon Developer Console で取得
    echo - AMAZON_CLIENT_SECRET: Amazon Developer Console で取得
    echo - AMAZON_REFRESH_TOKEN: SP-API認証フローで取得
    echo - AMAZON_SELLER_ID: Amazon Seller Central で確認
    echo - RAKUTEN_SERVICE_SECRET: 楽天デベロッパーポータルで取得
    echo - RAKUTEN_LICENSE_KEY: 楽天デベロッパーポータルで取得
    echo.
) else (
    echo ✅ .envファイルは既に存在します
)

REM 5. ディレクトリ構造作成
echo 📁 必要ディレクトリ作成中...
if not exist data mkdir data
if not exist logs mkdir logs
if not exist temp mkdir temp
if not exist config mkdir config

REM 6. 初期セットアップ実行
echo 🔧 初期セットアップ実行中...
python main.py setup
if errorlevel 1 (
    echo ⚠️ 初期セットアップでエラーが発生しました（.envファイル確認が必要な可能性があります）
)

REM 7. システム状況確認
echo 📊 システム状況確認中...
python main.py status

echo.
echo 🎉 Windows クイックスタート完了！
echo ==================================================
echo.
echo 🔑 次のステップ:
echo 1. .env ファイルを編集してAPIキーを設定
echo    コマンド: notepad .env
echo.
echo 2. システム確認コマンド:
echo    python main.py status    # システム状況確認
echo    python main.py test      # 統合テスト実行
echo    python main.py dashboard # ダッシュボード起動
echo.
echo 📚 詳細なガイド:
echo - セットアップ: SETUP_GUIDE.md
echo - 運用方法: OPERATION_MANUAL.md
echo - プロジェクト概要: README.md
echo.
echo 🎯 目標: 月次¥1,327,500+の利益向上！
echo ⚡ 作業効率化: 70-80%%削減
echo 💰 投資回収期間: 2-3ヶ月
echo.
echo 📝 APIキー設定が完了したら、Enterキーを押してシステムテストを実行してください...
pause >nul

echo 🧪 システムテスト実行中...
python main.py test

echo.
echo 🚀 システム準備完了！ダッシュボードを起動しますか？ (Y/N)
set /p choice="選択: "
if /i "%choice%"=="Y" (
    echo 📊 ダッシュボード起動中...
    python main.py dashboard
)

echo.
echo 👋 セットアップ完了！EC自動化システムで利益最大化を実現しましょう！
pause
