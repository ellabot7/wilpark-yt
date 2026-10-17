# 윌팍 채널 최근 영상 N편(이미 한 것·쇼츠 빼고)을 Gemini 로 한 번씩만 봄 → out/{ID}/summary.md, charts.json, meta.json, 차트장면_바로가기.md
import json, os, re, subprocess, sys, time
import xml.etree.ElementTree as ET
import requests
CH = "UCKjsuHBhmOHkIgVP4o4LfTQ"
n, done_dir, out = int(sys.argv[1]), sys.argv[2], sys.argv[3]
KEY = os.environ["GEMINI_API_KEY"]
ns = {"a": "http://www.w3.org/2005/Atom", "yt": "http://www.youtube.com/xml/schemas/2015", "m": "http://search.yahoo.com/mrss/"}
r = requests.get("https://www.youtube.com/feeds/videos.xml", params={"channel_id": CH}, timeout=30)
r.raise_for_status()
vids = []
for e in ET.fromstring(r.content).findall("a:entry", ns):
    vid = e.findtext("yt:videoId", "", ns); title = e.findtext("a:title", "", ns)
    link = e.find("a:link", ns).get("href", "")
    if "/shorts/" in link or os.path.exists(f"{done_dir}/{vid}/charts.json"):
        continue
    if any(v["title"] == title for v in vids):          # 같은 제목 다시 올린 것
        continue
    vids.append(dict(id=vid, title=title, date=e.findtext("a:published", "", ns)[:10]))
vids = vids[:n]
print("대상", [(v["date"], v["title"][:30]) for v in vids])
PROMPT = """이 영상은 한국 주식 유튜버 '윌팍'의 방송이다. 한국어로 답하고, JSON 하나만 출력해.
{"summary_md": "마크다운. 1) 전체 요약 10줄 2) 시간 순서 정리 [분:초] 단위: 이야기, 언급 종목·지수, 매수/매도 판단과 근거(차트 모양, 이평선, 추세선, 거래량, 재료) 3) 윌팍의 매매 원칙·습관 인용(시각 포함) 4) 언급 종목 표(종목명|시각|한 말|판단)",
 "charts": [{"t":"분:초","end":"분:초","name":"종목/지수","code":"종목코드(화면에 보일 때만, 아니면 null)","period":"1분봉/일봉 등","what":"차트에 보이는 것 한 줄(이평선, 추세선, B/S 표시, 손글씨, 가격 등)","said":"그때 한 말 요지 한 줄","good":true}]}
charts 는 화면에 주식 차트가 보이는 장면 전부. 같은 차트가 이어지면 한 번만, 종목·주기·확대가 바뀌면 새로. good = 고수 차트 공부 자료로 볼 만한지."""
def sec(s):
    v = 0
    for x in s.split(":"):
        v = v * 60 + int(x)
    return v
for v in vids:
    body = {"contents": [{"parts": [{"file_data": {"file_uri": f"https://www.youtube.com/watch?v={v['id']}"}}, {"text": PROMPT}]}],
            "generationConfig": {"temperature": 0.2, "maxOutputTokens": 60000, "responseMimeType": "application/json"}}
    res = None
    for model in [m for _ in range(5) for m in ("gemini-3.8-flash", "gemini-flash-latest")]:
        try:
            rr = requests.post(f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={KEY}", json=body, timeout=900)
        except requests.RequestException as ex:                 # 연결 끊김 → 잠시 뒤 다시
            print(v["id"], model, "연결 오류", ex); time.sleep(60); continue
        print(v["id"], model, rr.status_code)
        if rr.ok:
            try:
                txt = "".join(p.get("text", "") for p in rr.json()["candidates"][0]["content"]["parts"])
                res = json.loads(txt); break
            except Exception as ex:
                print("응답 이상", ex, rr.text[:300])
        else:
            print(rr.text[:300])
            if rr.status_code == 429 and "per day" in rr.text.lower():
                sys.exit(0)
        time.sleep(60)
    if not res:
        continue
    d = f"{out}/{v['id']}"; os.makedirs(d, exist_ok=True)
    json.dump(v, open(f"{d}/meta.json", "w"), ensure_ascii=False, indent=1)
    open(f"{d}/summary.md", "w").write(f"# {v['date']} {v['title']}\n\nhttps://youtu.be/{v['id']}\n\n" + res.get("summary_md", ""))
    ch = res.get("charts", [])
    json.dump(ch, open(f"{d}/charts.json", "w"), ensure_ascii=False, indent=1)
    L = [f"# {v['date']} 「{v['title']}」 차트 장면 바로가기", "",
         "누르면 그 시각(2초 앞)부터 재생됩니다. 화질 1080p로 바꾸고 멈춘 뒤 스샷하세요. ⭐ = 공부 자료로 볼 만한 장면. 시각은 Gemini 가 적은 것이라 몇 초 어긋날 수 있음.", "",
         "| | 시각 | 종목·지수 | 봉 | 화면 | 윌팍 말 |", "|---|---|---|---|---|---|"]
    for x in ch:
        try:
            s = max(0, sec(x["t"]) - 2)
        except Exception:
            continue
        L.append(f'| {"⭐" if x.get("good") else ""} | [{x["t"]}](https://www.youtube.com/watch?v={v["id"]}&t={s}s) | {x.get("name","")} | {x.get("period","")} | {x.get("what","")} | {x.get("said","")} |')
    open(f"{d}/차트장면_바로가기.md", "w").write("\n".join(L) + "\n")
    time.sleep(20)
