@echo off
chcp 65001 > nul
echo 🚀 EC自動化システム - セットアップ開始
echo ===============================================

echo.
echo 📁 プロジェクトディレクトリ確認中...
cd /d "%~dp0"
echo 現在の場所: %CD%

echo.
echo 🐍 Python環境確認中...
python --version
if errorlevel 1 (
    echo ❌ Pythonがインストールされていません
    echo 💡 Python 3.8以上をインストールしてください
    pause
    exit /b 1
)

echo.
echo 📦 依存関係インストール中...
pip install -r requirements.txt
if errorlevel 1 (
    echo ⚠️ 依存関係のインストールでエラーが発生しました
    echo 💡 pip install --upgrade pip を実行してから再度お試しください
)

echo.
echo ⚙️ 環境セットアップ実行中...
python main.py setup

echo.
echo 🧪 システムテスト実行中...
python main.py test

echo.
echo 🎉 セットアップ完了！
echo.
echo 📊 ダッシュボードを起動するには:
echo    python main.py dashboard
echo.
echo 🤖 AI分析を実行するには:
echo    python main.py ai
echo.
echo 📋 システム状況を確認するには:
echo    python main.py status
echo.
pause
