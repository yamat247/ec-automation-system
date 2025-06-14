@echo off
REM 🚀 EC自動化システム - Notion連携自動化バッチファイル
REM 毎日22:00にタスクスケジューラで実行推奨

echo 📊 EC自動化システム - Notion連携開始
echo ==========================================

REM 1. プロジェクトディレクトリに移動
cd /d "%~dp0"
echo 📍 ディレクトリ: %CD%

REM 2. 自動化エンジン実行（データ生成）
echo 🤖 自動化エンジン実行中...
python main.py automation
if errorlevel 1 (
    echo ⚠️ 自動化エンジンでエラーが発生しました
)

REM 3. Notion同期実行
echo 📊 Notion同期実行中...
python main.py notion
if errorlevel 1 (
    echo ❌ Notion同期でエラーが発生しました
    goto :error
)

echo ✅ Notion連携完了！
echo 💡 Notionワークスペースでデータを確認してください
goto :end

:error
echo ❌ エラーが発生しました
echo 💡 以下を確認してください:
echo   - .envファイルのNotion設定
echo   - インターネット接続
echo   - Notion Integration権限
pause
exit /b 1

:end
echo 🎉 EC自動化システム - Notion連携完了
echo 📅 次回実行: 明日22:00（タスクスケジューラ設定時）
REM pause
