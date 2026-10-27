# 네이버 일봉 받기 (이 창고 GitHub 서버에서만 됨): python price_fetch.py 0011A0,000490 out/prices → {코드}.csv date,open,high,low,close,volume
import os, re, sys
import requests
codes, out = sys.argv[1].split(","), sys.argv[2]
os.makedirs(out, exist_ok=True)
for c in codes:
    c = c.strip()
    r = requests.get("https://fchart.stock.naver.com/sise.nhn", params={"symbol": c, "timeframe": "day", "count": 1500, "requestType": 0},
                     headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
    rows = re.findall(r'data="([^"]+)"', r.text)
    print(c, r.status_code, len(rows))
    with open(f"{out}/{c}.csv", "w") as f:
        f.write("date,open,high,low,close,volume\n")
        for x in rows:
            f.write(x.replace("|", ",") + "\n")
