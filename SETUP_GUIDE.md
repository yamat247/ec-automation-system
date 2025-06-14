# 🚀 EC自動化システム完全セットアップガイド

## 📋 セットアップチェックリスト

### ✅ 1. 基本環境準備
- [ ] Python 3.8以上インストール済み
- [ ] Git インストール済み
- [ ] GitHubアカウント作成済み

### ✅ 2. リポジトリクローン
```bash
git clone https://github.com/yamat247/ec-automation-system.git
cd ec-automation-system
```

### ✅ 3. Python依存関係インストール
```bash
pip install -r requirements.txt
```

### ✅ 4. 環境変数設定（重要）
```bash
# .envファイルを作成
copy .env.example .env

# .envファイルを編集（下記の実際の値を設定）
notepad .env
```

## 🔑 必要なAPIキー情報

### 🤖 AI API設定
- **Gemini API Key**: Google AI Studio で取得
- **Claude API Key**: Anthropic Console で取得

### 🛒 Amazon SP-API設定
- **Client ID**: Amazon Developer Console で取得
- **Client Secret**: Amazon Developer Console で取得
- **Refresh Token**: SP-API認証フローで取得
- **Seller ID**: Amazon Seller Central で確認

### 🟢 楽天API設定
- **Service Secret**: 楽天デベロッパーポータルで取得
- **License Key**: 楽天デベロッパーポータルで取得

## 🚀 システム起動手順

### ステップ1: 初期セットアップ
```bash
python main.py setup
```

### ステップ2: システム状況確認
```bash
python main.py status
```

### ステップ3: 統合テスト実行
```bash
python main.py test
```

### ステップ4: ダッシュボード起動
```bash
python main.py dashboard
```

## 📊 期待される効果

### 💰 利益向上効果
- **月次利益向上**: ¥1,327,500+ (18.1%増)
- **作業効率化**: 70-80%削減
- **投資回収期間**: 2-3ヶ月
- **年間ROI**: 200-300%

### 🔄 自動化される作業
- 在庫監視・アラート
- 価格競合分析
- 商品ランキング追跡
- レビュー分析
- 売上レポート生成

## ⚠️ 重要な注意事項

### セキュリティ
- `.env`ファイルは絶対にGitHubにアップロードしない
- APIキーは定期的に更新する
- 本番環境では`DEBUG_MODE=false`に設定

### 運用
- 毎日のシステムヘルスチェック
- 週次の売上分析レポート確認
- 月次のAI推奨アクション実行

## 🛠️ トラブルシューティング

### よくある問題
1. **API接続エラー**: `.env`ファイルのAPIキー確認
2. **依存関係エラー**: `pip install -r requirements.txt`再実行
3. **権限エラー**: Amazon・楽天の開発者アカウント権限確認

### サポート
- GitHub Issues: バグ報告・機能要望
- ドキュメント: README.md 参照
- ログ確認: `./logs/` ディレクトリ

## 🎯 成功指標

### システム正常動作確認
- [ ] `python main.py status` で全API接続✅表示
- [ ] `python main.py test` で統合テスト成功
- [ ] ダッシュボードでリアルタイムデータ表示
- [ ] AI分析による具体的改善提案の取得

### ビジネス成果確認
- [ ] 月次売上前年同期比増加
- [ ] 作業時間削減の実感
- [ ] 利益率改善の数値確認
- [ ] 競合優位性の向上

---
*最終更新: 2025年6月15日*
