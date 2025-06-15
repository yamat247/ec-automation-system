#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EC自動化システム 設定管理
セキュアな環境変数・設定管理モジュール
"""

import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

class ECAutomationConfig:
    """EC自動化システム設定クラス"""
    
    def __init__(self):
        """設定初期化"""
        # .envファイル読み込み
        env_path = Path(__file__).parent.parent / '.env'
        load_dotenv(env_path)
        
        # デバッグモード
        self.debug_mode = os.getenv('DEBUG_MODE', 'false').lower() == 'true'
        
        # AI API設定
        self.gemini_api_key = os.getenv('GEMINI_API_KEY')
        self.claude_api_key = os.getenv('CLAUDE_API_KEY')
        
        # Amazon SP-API設定
        self.amazon_client_id = os.getenv('AMAZON_CLIENT_ID')
        self.amazon_client_secret = os.getenv('AMAZON_CLIENT_SECRET')
        self.amazon_refresh_token = os.getenv('AMAZON_REFRESH_TOKEN')
        self.amazon_seller_id = os.getenv('AMAZON_SELLER_ID')
        
        # 楽天API設定
        self.rakuten_service_secret = os.getenv('RAKUTEN_SERVICE_SECRET')
        self.rakuten_license_key = os.getenv('RAKUTEN_LICENSE_KEY')
        
        # システム設定
        self.log_level = os.getenv('LOG_LEVEL', 'INFO')
        self.database_path = os.getenv('DATABASE_PATH', './data/ec_automation.db')

        # Notion設定
        self.notion_token = os.getenv('NOTION_TOKEN')
        self.notion_database_id = os.getenv('NOTION_DATABASE_ID')
        
        # バリデーション実行
        self.validate_config()
    
    def validate_config(self):
        """設定バリデーション"""
        missing_configs = []
        
        # 必須設定チェック
        required_configs = {
            'GEMINI_API_KEY': self.gemini_api_key,
            'CLAUDE_API_KEY': self.claude_api_key,
            'AMAZON_CLIENT_ID': self.amazon_client_id,
            'AMAZON_CLIENT_SECRET': self.amazon_client_secret,
            'RAKUTEN_SERVICE_SECRET': self.rakuten_service_secret,
            'RAKUTEN_LICENSE_KEY': self.rakuten_license_key
        }
        
        for config_name, config_value in required_configs.items():
            if not config_value:
                missing_configs.append(config_name)
        
        if missing_configs:
            print(f"⚠️ 以下の環境変数が設定されていません: {', '.join(missing_configs)}")
            print("💡 .env.example を参考に .env ファイルを作成してください")
            
            if not self.debug_mode:
                raise ValueError(f"必須設定が不足しています: {missing_configs}")
    
    @property
    def amazon_config(self) -> dict:
        """Amazon設定取得"""
        return {
            'client_id': self.amazon_client_id,
            'client_secret': self.amazon_client_secret,
            'refresh_token': self.amazon_refresh_token,
            'seller_id': self.amazon_seller_id
        }
    
    @property
    def rakuten_config(self) -> dict:
        """楽天設定取得"""
        return {
            'service_secret': self.rakuten_service_secret,
            'license_key': self.rakuten_license_key
        }
    
    @property
    def ai_config(self) -> dict:
        """AI設定取得"""
        return {
            'gemini_api_key': self.gemini_api_key,
            'claude_api_key': self.claude_api_key
        }
    
    def get_database_path(self) -> Path:
        """データベースパス取得"""
        db_path = Path(self.database_path)
        db_path.parent.mkdir(parents=True, exist_ok=True)
        return db_path
    
    def is_production(self) -> bool:
        """本番環境判定"""
        return not self.debug_mode
    
    def __repr__(self):
        """設定情報表示（機密情報はマスク）"""
        return f"""
EC自動化システム設定:
├── デバッグモード: {self.debug_mode}
├── ログレベル: {self.log_level}
├── データベース: {self.database_path}
├── Gemini API: {'✅ 設定済み' if self.gemini_api_key else '❌ 未設定'}
├── Claude API: {'✅ 設定済み' if self.claude_api_key else '❌ 未設定'}
├── Amazon API: {'✅ 設定済み' if self.amazon_client_id else '❌ 未設定'}
├── 楽天API: {'✅ 設定済み' if self.rakuten_service_secret else '❌ 未設定'}
└── Notion連携: {'✅ 設定済み' if self.notion_database_id else '❌ 未設定'}
        """.strip()

# グローバル設定インスタンス
config = ECAutomationConfig()

def get_config() -> ECAutomationConfig:
    """設定取得（シングルトン）"""
    return config

if __name__ == "__main__":
    # 設定テスト
    print("🔧 EC自動化システム設定テスト")
    print(config)
