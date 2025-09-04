from flask import Flask, request, render_template
import requests
import os

app = Flask(__name__)

def get_client_ip():
    """CloudFlareやリバースプロキシ対応で実IPを取得"""
    x_forwarded_for = request.headers.get("X-Forwarded-For")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0].strip()
    else:
        ip = request.remote_addr
    return ip

@app.route("/")
def index():
    user_ip = get_client_ip()

    try:
        # ip-api.com を使い日本語で返す
        resp = requests.get(f"http://ip-api.com/json/{user_ip}?lang=ja", timeout=3).json()
        prefecture = resp.get("regionName", "不明")  # 都道府県
        city = resp.get("city", "不明")            # 市区町村
    except:
        prefecture = "不明"
        city = "不明"

    return render_template("index.html", prefecture=prefecture, city=city)

if __name__ == "__main__":
    # ローカル用テスト
    app.run(debug=False)
