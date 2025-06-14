@echo off
REM 🚀 EC自動化システム統合 - Notion自動同期バッチファイル
REM 毎日22:00にタスクスケジューラで実行推奨

echo 📊 EC自動化システム統合 - Notion連携開始
echo ================================================

REM 1. プロジェクトディレクトリに移動
cd /d "%~dp0"
echo 📍 ディレクトリ: %CD%

REM 2. システム状況確認
echo 🔍 システム状況確認中...
python main.py status
if errorlevel 1 (
    echo ⚠️ システム設定に問題があります
)

REM 3. 自動化エンジン実行（データ生成）
echo 🤖 自動化エンジン実行中...
python main.py automation
if errorlevel 1 (
    echo ⚠️ 自動化エンジンでエラーが発生しました
)

REM 4. EC統合Notion同期実行
echo 📊 EC統合Notion同期実行中...
python main.py notion
if errorlevel 1 (
    echo ❌ Notion同期でエラーが発生しました
    goto :error
)

echo ✅ EC統合Notion連携完了！
echo 💡 Notionワークスペースでデータを確認してください
echo 📈 Amazon・楽天・AI分析データが全て統合されました
goto :end

:error
echo ❌ エラーが発生しました
echo 💡 以下を確認してください:
echo   - .envファイルのNotion設定（NOTION_TOKEN, NOTION_DATABASE_ID）
echo   - インターネット接続
echo   - Notion Integration権限
echo   - システム構成ファイル
pause
exit /b 1

:end
echo 🎉 EC自動化システム統合 - Notion連携完了
echo 📅 次回実行: 明日22:00（タスクスケジューラ設定時）
echo 📊 統合データベースID: 212e415da2cf8012b4f5cbea3cadb458
REM pause
