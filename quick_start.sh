#!/bin/bash
# 🚀 EC自動化システム - クイックスタートスクリプト
# 使用方法: bash quick_start.sh

echo "🚀 EC自動化システム - クイックスタート開始"
echo "=================================================="

# 1. 現在のディレクトリ確認
echo "📍 現在のディレクトリ: $(pwd)"

# 2. Python環境確認
echo "🐍 Python環境確認..."
python --version
if [ $? -ne 0 ]; then
    echo "❌ Python がインストールされていません"
    exit 1
fi

# 3. 依存関係インストール
echo "📦 依存関係インストール中..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ 依存関係のインストールに失敗しました"
    exit 1
fi

# 4. .envファイル作成
echo "⚙️ 環境変数ファイル準備中..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✅ .envファイルを作成しました"
    echo ""
    echo "🔑 重要: 次に .env ファイルを編集してAPIキーを設定してください"
    echo "📝 編集コマンド: notepad .env (Windows) または nano .env (Linux/Mac)"
    echo ""
    echo "必要なAPIキー:"
    echo "- GEMINI_API_KEY: Google AI Studio で取得"
    echo "- CLAUDE_API_KEY: Anthropic Console で取得"
    echo "- AMAZON_CLIENT_ID: Amazon Developer Console で取得"
    echo "- AMAZON_CLIENT_SECRET: Amazon Developer Console で取得"
    echo "- AMAZON_REFRESH_TOKEN: SP-API認証フローで取得"
    echo "- AMAZON_SELLER_ID: Amazon Seller Central で確認"
    echo "- RAKUTEN_SERVICE_SECRET: 楽天デベロッパーポータルで取得"
    echo "- RAKUTEN_LICENSE_KEY: 楽天デベロッパーポータルで取得"
    echo ""
else
    echo "✅ .envファイルは既に存在します"
fi

# 5. ディレクトリ構造作成
echo "📁 必要ディレクトリ作成中..."
mkdir -p data logs temp config

# 6. 初期セットアップ実行
echo "🔧 初期セットアップ実行中..."
python main.py setup
if [ $? -ne 0 ]; then
    echo "⚠️ 初期セットアップでエラーが発生しました（.envファイル確認が必要な可能性があります）"
fi

# 7. システム状況確認
echo "📊 システム状況確認中..."
python main.py status

echo ""
echo "🎉 クイックスタート完了！"
echo "=================================================="
echo ""
echo "🔑 次のステップ:"
echo "1. .env ファイルを編集してAPIキーを設定"
echo "   Windows: notepad .env"
echo "   Linux/Mac: nano .env"
echo ""
echo "2. システム確認コマンド:"
echo "   python main.py status    # システム状況確認"
echo "   python main.py test      # 統合テスト実行"
echo "   python main.py dashboard # ダッシュボード起動"
echo ""
echo "📚 詳細なガイド:"
echo "- セットアップ: SETUP_GUIDE.md"
echo "- 運用方法: OPERATION_MANUAL.md"
echo "- プロジェクト概要: README.md"
echo ""
echo "🎯 目標: 月次¥1,327,500+の利益向上！"
echo "⚡ 作業効率化: 70-80%削減"
echo "💰 投資回収期間: 2-3ヶ月"
