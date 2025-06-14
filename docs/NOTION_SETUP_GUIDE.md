# 🚀 Notion連携完全セットアップガイド

## 📋 Step 1: Notion Integrationの作成

### 1. Notion Developer Portal にアクセス
```
https://www.notion.so/my-integrations
```

### 2. 新しいIntegration作成
1. **「+ New integration」**をクリック
2. **Integration名**: `EC自動化システム`
3. **Workspace**: あなたのNotionワークスペース選択
4. **Submit**をクリック

### 3. APIトークン取得
- **Internal Integration Token**をコピー
- これが`NOTION_TOKEN`になります

## 📊 Step 2: Notionデータベース作成

### 1. 新しいページ作成
```
ページタイトル: 📊 EC自動化システム ダッシュボード
```

### 2. データベース追加
1. `/database`と入力
2. **「Full page」**選択
3. データベース名: `日次売上レポート`

### 3. プロパティ設定
以下のプロパティを追加：

| プロパティ名 | タイプ | フォーマット |
|-------------|--------|-------------|
| 日付 | Date | - |
| 総売上 | Number | Yen |
| 注文数 | Number | - |
| 平均注文額 | Number | Yen |
| 利益率 | Number | Percent |
| 今日の利益 | Number | Yen |
| Amazon売上 | Number | Yen |
| Amazon注文数 | Number | - |
| 楽天売上 | Number | Yen |
| 楽天注文数 | Number | - |
| 在庫充足率 | Number | Percent |
| 要補充商品 | Number | - |
| 総商品数 | Number | - |
| AI提案数 | Number | - |
| 高優先度提案 | Number | - |
| 期待利益向上 | Number | Yen |
| ステータス | Select | 正常稼働/要注意/異常/メンテナンス中 |
| 自動化エンジン | Select | 稼働中/停止中/エラー |
| Amazon API | Select | 正常/警告/エラー |
| 楽天API | Select | 正常/警告/エラー |
| AI分析 | Select | 正常/警告/エラー |

### 4. データベースID取得
1. データベースページのURL確認
```
https://www.notion.so/your-workspace/DATABASE_ID?v=...
```
2. `DATABASE_ID`部分をコピー
3. これが`NOTION_DATABASE_ID`になります

## 🔧 Step 3: 環境変数設定

### .envファイルに追加
```bash
# Notion API設定
NOTION_TOKEN=secret_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
NOTION_DATABASE_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

## 🎯 Step 4: Integration権限設定

### 1. データベースページでIntegration招待
1. データベースページの右上「**•••**」メニュー
2. **「Add connections」**選択
3. 作成した`EC自動化システム`Integration選択
4. **「Confirm」**クリック

### 2. 権限確認
- **Read content**: ✅
- **Update content**: ✅
- **Insert content**: ✅

## 🚀 Step 5: テスト実行

### 1. 連携テスト
```bash
python -c "
from src.notion_enhanced_integration import NotionECIntegration
import asyncio

async def test():
    notion = NotionECIntegration()
    if notion.validate_notion_config():
        print('✅ 設定OK')
        await notion.sync_daily_report()
    else:
        print('❌ 設定不備')

asyncio.run(test())
"
```

### 2. 日次同期実行
```bash
python src/notion_enhanced_integration.py
```

## 📅 Step 6: 自動化設定

### Windowsタスクスケジューラ
```batch
# daily_notion_sync.bat
@echo off
cd C:\path\to\ec-automation-system
python src/notion_enhanced_integration.py
```

**スケジュール**: 毎日22:00実行

### Linux/Mac cron設定
```bash
# 毎日22:00に実行
0 22 * * * cd /path/to/ec-automation-system && python src/notion_enhanced_integration.py
```

## 🎨 Step 7: ダッシュボードカスタマイズ

### ビュー作成
1. **売上トレンドビュー**
   - フィルター: 過去30日
   - ソート: 日付降順
   - グラフ: 線グラフ（総売上）

2. **アラートビュー** 
   - フィルター: ステータス = 要注意 OR 異常
   - ソート: 日付降順

3. **月次サマリービュー**
   - フィルター: 今月
   - グループ: 週別
   - 集計: 売上合計

### テンプレート構造
```
📊 EC自動化システム ダッシュボード
├── 📈 今日の実績サマリー
├── 📊 埋め込みデータベース（売上トレンド）
├── 🤖 AI推奨アクション
├── ⚙️ システム状況
└── 📅 今日のタスク
```

## 💡 活用のコツ

### 1. 朝のルーティン（5分）
- ダッシュボード確認
- AI提案確認・実行判断
- 在庫アラート対応

### 2. 週次レビュー（15分）
- 週間トレンド分析
- 月次目標進捗確認
- AI提案効果測定

### 3. 月次戦略会議（30分）
- データ基づく次月戦略立案
- システム改善点抽出
- 新機能検討

## 🔧 トラブルシューティング

### よくある問題

1. **「integration_token is invalid」**
   - トークン再生成・コピー確認
   - .envファイル保存確認

2. **「database_id could not be found」**
   - データベースID確認
   - Integration権限確認

3. **「property does not exist」**
   - プロパティ名の正確性確認
   - データベース構造再確認

### サポート
- **設定サポート**: SETUP_GUIDE.md
- **技術サポート**: GitHub Issues
- **Notion公式**: https://developers.notion.com/

---

## 🎉 完了チェックリスト

- [ ] Notion Integration作成・トークン取得
- [ ] Notionデータベース作成・プロパティ設定
- [ ] データベースID取得
- [ ] .envファイル設定
- [ ] Integration権限設定
- [ ] 連携テスト成功
- [ ] 日次同期動作確認
- [ ] 自動化スケジュール設定
- [ ] ダッシュボードカスタマイズ

**これで、EC自動化システムとNotionの完全連携が完了です！**

🎯 **期待効果**: データドリブンなEC運営による月次¥1,327,500+の利益向上
