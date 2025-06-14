#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Amazon SP-API 接続モジュール - セキュア版
"""

import requests
import json
import webbrowser
from datetime import datetime, timedelta
from pathlib import Path
import sys

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from config.settings import get_config

class AmazonSPAPIConnector:
    def __init__(self):
        """Amazon SP-API接続クラス初期化"""
        self.config = get_config()
        self.amazon_config = self.config.amazon_config
        
        # SP-API エンドポイント
        self.api_base_url = "https://sellingpartnerapi-fe.amazon.com"
        self.auth_base_url = "https://api.amazon.com/auth/o2"
        
        # 日本マーケットプレイスID
        self.marketplace_id = "A1VC38T7YXB528"
        
        print("🔍 Amazon SP-API コネクター初期化完了")
    
    def get_authorization_url(self):
        """認証URL生成"""
        if not self.amazon_config['client_id']:
            raise ValueError("Amazon Client IDが設定されていません")
        
        redirect_uri = "https://localhost:3000/callback"
        scope = "sellingpartnerapi::migration"
        state = "state123"
        
        auth_url = (
            f"https://sellercentral.amazon.co.jp/apps/authorize/consent"
            f"?client_id={self.amazon_config['client_id']}"
            f"&scope={scope}"
            f"&response_type=code"
            f"&redirect_uri={redirect_uri}"
            f"&state={state}"
        )
        
        return auth_url
    
    def get_sales_data(self, days=7):
        """売上データ取得（モック版）"""
        print("🧪 モック売上データを使用")
        
        return {
            "total_sales": 1050000,  # 7日間合計
            "total_orders": 84,
            "avg_order_value": 12500,
            "daily_sales": {
                "2025-06-08": 180000,
                "2025-06-09": 165000,
                "2025-06-10": 140000,
                "2025-06-11": 175000,
                "2025-06-12": 155000,
                "2025-06-13": 125000,
                "2025-06-14": 110000
            },
            "period_days": 7,
            "data_source": "mock"
        }
    
    def check_connection_status(self):
        """接続状況確認"""
        config_check = {
            "client_id": bool(self.amazon_config['client_id']),
            "client_secret": bool(self.amazon_config['client_secret']),
            "refresh_token": bool(self.amazon_config['refresh_token']),
            "seller_id": bool(self.amazon_config['seller_id'])
        }
        
        all_configured = all(config_check.values())
        
        status = {
            "configured": all_configured,
            "missing_config": [k for k, v in config_check.items() if not v],
            "ready_for_api_calls": all_configured
        }
        
        return status

if __name__ == "__main__":
    connector = AmazonSPAPIConnector()
    status = connector.check_connection_status()
    print(f"Amazon設定状況: {status}")
    
    sales_data = connector.get_sales_data()
    print(f"売上データ: ¥{sales_data['total_sales']:,}")