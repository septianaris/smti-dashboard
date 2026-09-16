# -*- coding: utf-8 -*-
"""
Script deploy otomatis 1-klik ke Vercel Production
"""
import urllib.request
import json
import os

token_file = os.path.join(os.path.dirname(__file__), ".vercel_token")
if os.path.exists(token_file):
    with open(token_file, "r", encoding="utf-8-sig") as f:
        TOKEN = f.read().strip().replace("\ufeff", "")
else:
    TOKEN = os.environ.get("VERCEL_TOKEN", "").strip().replace("\ufeff", "")

if not TOKEN:
    print("[ERROR] Token Vercel tidak ditemukan di .vercel_token atau VERCEL_TOKEN!")
    exit(1)

print("[INFO] Membaca file index.html terbaru...")
with open(os.path.join(os.path.dirname(__file__), "index.html"), "r", encoding="utf-8") as f:
    html_content = f.read()

payload = {
    "name": "smti-dashboard",
    "files": [
        {
            "file": "index.html",
            "data": html_content
        }
    ],
    "projectSettings": {
        "framework": None
    },
    "target": "production"
}

print("[INFO] Mengunggah dan mem-publish ke Vercel Production...")
req = urllib.request.Request(
    "https://api.vercel.com/v13/deployments",
    data=json.dumps(payload).encode("utf-8"),
    headers={
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json",
        "User-Agent": "SMTI-Deployer"
    },
    method="POST"
)

try:
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode())
        print("[SUCCESS] DEPLOYMENT BERHASIL!")
        print("URL Resmi     : https://smti-pupuk-kujang.vercel.app")
        print("URL Alternatif: https://smti-dashboard-smti2.vercel.app")
        print("Status        :", res.get("readyState") or res.get("status"))
except Exception as e:
    print("[ERROR] Terjadi kesalahan saat deploy:", e)
