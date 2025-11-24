import time
import hmac
import hashlib
import os

import requests

"""
本檔僅用於本機測試 Bitfinex /v2/auth/r/wallets。
為避免把真實 API Key 推到 Git，請使用環境變數設定憑證：

    BITFINEX_API_KEY
    BITFINEX_API_SECRET

在 PowerShell 中設定範例：

    setx BITFINEX_API_KEY "your_api_key_here"
    setx BITFINEX_API_SECRET "your_api_secret_here"
    # 重新開啟終端機後執行：
    python test_bitfinex_wallets.py
"""

BASE_URL = "https://api.bitfinex.com"
ENDPOINT = "/v2/auth/r/wallets"


def call_wallets():
    api_key = os.getenv("BITFINEX_API_KEY")
    api_secret = os.getenv("BITFINEX_API_SECRET")
    if not api_key or not api_secret:
        print("請先在環境變數中設定 BITFINEX_API_KEY / BITFINEX_API_SECRET")
        return

    url = BASE_URL + ENDPOINT
    nonce = str(int(time.time() * 1000))
    body = ""

    path_for_sig = "/api/2" + ENDPOINT
    payload = f"{path_for_sig}{nonce}{body}".encode()

    signature = hmac.new(api_secret.encode(), payload, hashlib.sha384).hexdigest()

    headers = {
        "bfx-apikey": api_key,
        "bfx-signature": signature,
        "bfx-nonce": nonce,
        "Content-Type": "application/json",
    }

    resp = requests.post(url, headers=headers, data=body)
    print("Status:", resp.status_code)
    print("Body:", resp.text)


if __name__ == "__main__":
    call_wallets()