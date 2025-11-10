import requests
import hmac
import hashlib
import json
from typing import Optional, Dict, List, Any
from datetime import datetime
from app.core.config import settings


class BitfinexClient:
    """Bitfinex API 客戶端 (v2 認證)"""
    
    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = settings.BITFINEX_API_URL  # e.g. https://api.bitfinex.com/v2
    
    def _make_authenticated_request(
        self, 
        endpoint: str, 
        method: str = "POST",
        json_body: Optional[Dict] = None
    ) -> Dict:
        """發送 v2 認證請求"""
        url = f"{self.base_url}{endpoint}"
        path_for_sig = f"/api/2{endpoint}"
        nonce = str(int(datetime.now().timestamp() * 1000))
        # Bitfinex 簽名：path + nonce + body（無 body 時使用空字串）
        body_str = json.dumps(json_body, separators=(",", ":")) if json_body else ""
        signature_payload = f"{path_for_sig}{nonce}{body_str}".encode()
        signature = hmac.new(self.api_secret.encode(), signature_payload, hashlib.sha384).hexdigest()
        
        headers = {
            "bfx-apikey": self.api_key,
            "bfx-signature": signature,
            "bfx-nonce": nonce,
            "Content-Type": "application/json"
        }
        
        try:
            if method.upper() == "POST":
                response = requests.post(url, headers=headers, data=body_str)
            else:
                response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            detail = getattr(e.response, "text", str(e)) if getattr(e, "response", None) else str(e)
            raise Exception(f"Bitfinex API 請求失敗: {detail}")
    
    def get_wallets(self) -> List[Dict[str, Any]]:
        return self._make_authenticated_request("/auth/r/wallets") or []
    
    def get_funding_offers(self, currency: str = "USD") -> List[Dict[str, Any]]:
        symbol = f"f{currency}"
        return self._make_authenticated_request(f"/auth/r/funding/offers/{symbol}") or []
    
    def get_funding_credits(self, currency: str = "USD") -> List[Dict[str, Any]]:
        symbol = f"f{currency}"
        return self._make_authenticated_request(f"/auth/r/funding/credits/{symbol}") or []
    
    def get_loans(self, currency: str = "USD") -> List[Dict[str, Any]]:
        credits = self.get_funding_credits(currency)
        loans: List[Dict[str, Any]] = []
        for credit in credits:
            if isinstance(credit, list) and len(credit) >= 12:
                loans.append({
                    "id": credit[0],
                    "symbol": credit[1],
                    "side": credit[2],
                    "created_at": credit[3],
                    "amount": credit[4],
                    "rate": credit[5],
                    "period": credit[6],
                    "maker": credit[7],
                    "taker": credit[8],
                    "status": credit[10] if len(credit) > 10 else None,
                })
        return loans
    
    def get_trades(self, symbol: str = "USD", limit: int = 250) -> List[Dict[str, Any]]:
        return self._make_authenticated_request(
            f"/auth/r/trades/{symbol}/hist",
            json_body={"limit": limit}
        ) or []
    
    def get_funding_trades(self, currency: str = "USD") -> List[Dict[str, Any]]:
        symbol = f"f{currency}"
        return self._make_authenticated_request(f"/auth/r/funding/trades/{symbol}/hist") or []
    
    def get_account_summary(self) -> Dict[str, Any]:
        wallets = self.get_wallets()
        total_balance: Dict[str, float] = {}
        funding_balance: Dict[str, float] = {}
        for wallet in wallets:
            if isinstance(wallet, list) and len(wallet) >= 3:
                wallet_type = wallet[0]
                currency = wallet[1]
                balance = wallet[2]
                if wallet_type == "funding":
                    funding_balance[currency] = funding_balance.get(currency, 0) + balance
                total_balance[currency] = total_balance.get(currency, 0) + balance
        return {
            "wallets": wallets,
            "total_balance": total_balance,
            "funding_balance": funding_balance
        }
    
    def get_user_info(self) -> Dict[str, Any]:
        result = self._make_authenticated_request("/auth/r/info/user")
        return result if isinstance(result, list) and len(result) > 0 else {}
