# app.py
from flask import Flask, request, render_template
import requests
import os

app = Flask(__name__)

IPINFO_TOKEN = os.getenv("IPINFO_TOKEN")  # .env に設定

def get_client_ip():
    """CloudFlareやリバースプロキシ対応で実IPを取得"""
    x_forwarded_for = request.headers.get("X-Forwarded-For")
    if x_forwarded_for:
        # 複数IPが来る場合は先頭を使用
        ip = x_forwarded_for.split(",")[0].strip()
    else:
        ip = request.remote_addr
    return ip

@app.route("/")
def index():
    user_ip = get_client_ip()

    # デバッグ用
    print("アクセスIP:", user_ip)

    # ipinfo.io でジオロケーション
    url = f"https://ipinfo.io/{user_ip}/json?token={IPINFO_TOKEN}"
    try:
        resp = requests.get(url, timeout=3).json()
        prefecture = resp.get("region", "不明")  # 都道府県
        city = resp.get("city", "不明")         # 市区町村
    except Exception as e:
        print("ジオロケーション取得エラー:", e)
        prefecture = "不明"
        city = "不明"

    return render_template("index.html", prefecture=prefecture, city=city)

if __name__ == "__main__":
    app.run(debug=True)
