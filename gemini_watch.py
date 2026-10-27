# Gemini 에게 유튜브 주소를 그대로 주고(구글이 직접 영상을 봄) 상세 요약 + 차트 장면 목록을 받음
import json, os, re, sys, time
import requests
vid, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
KEY = os.environ["GEMINI_API_KEY"]
URL = f"https://www.youtube.com/watch?v={vid}"
PROMPTS = {
    "summary.md": """이 영상은 한국 주식 유튜버 '윌팍'의 방송이다. 한국어로 아주 상세히 정리해 줘.
1) 전체 요약 (10줄)
2) 시간 순서 정리: [분:초] 단위로 나오는 이야기, 언급한 종목·지수, 매수/매도 판단, 근거(차트 모양, 이평선, 추세선, 거래량, 재료)를 빠짐없이
3) 윌팍의 매매 원칙·습관으로 볼 수 있는 말 (그대로 인용 + 시각)
4) 언급 종목 표: 종목명 | 시각 | 한 말 | 판단(매수/매도/관망)""",
    "charts.json": """이 영상에서 화면에 주식 차트가 보이는 장면을 모두 찾아 줘. 같은 차트가 계속 보이면 한 번만, 종목·주기·확대가 바뀌면 새로.
JSON 배열만 출력: [{"t":"분:초","end":"분:초","name":"종목/지수 이름","code":"종목코드(보이면)","period":"1분봉/3분봉/일봉/주봉 등","what":"차트에 보이는 것(이평선 색, 추세선, B/S 표시, 박스, 화살표 등) 한 줄","said":"그때 윌팍이 한 말 요지 한 줄","good":true/false (고수 차트 공부 자료로 볼 만한지)}]""",
}
ONLY = os.environ.get("ONLY", "")
# 질문 하나만 따로: ASK(질문), ASK_NAME(파일 이름), CLIP="시작초-끝초"(그 구간만 자세히, fps 1)
if os.environ.get("ASK"):
    PROMPTS = {os.environ.get("ASK_NAME") or "ask.md": os.environ["ASK"]}
    ONLY = ""
VM = {}
if re.fullmatch(r"\d+-\d+", os.environ.get("CLIP", "")):
    a, b = os.environ["CLIP"].split("-")
    VM = {"videoMetadata": {"startOffset": f"{a}s", "endOffset": f"{b}s", "fps": 1}}
for fn, prompt in PROMPTS.items():
    if ONLY and fn not in ONLY.split(","):
        continue
    body = {"contents": [{"parts": [{"file_data": {"file_uri": URL}, **VM}, {"text": prompt}]}],
            "generationConfig": {"temperature": 0.2, "maxOutputTokens": 32768}}
    if fn.endswith(".json"):
        body["generationConfig"]["responseMimeType"] = "application/json"
    done = False
    for model in [m for _ in range(4) for m in (os.environ.get("MODELS") or "gemini-3.8-flash,gemini-flash-latest").split(",")]:  # 붐비면(503) 쉬었다 다시
        if done:
            break
        try:
            r = requests.post(f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={KEY}",
                              json=body, timeout=900)
        except requests.RequestException as e:          # 연결 끊김도 쉬었다 다시
            print(fn, model, "연결 끊김", e); time.sleep(60); continue
        print(fn, model, r.status_code)
        if r.ok:
            try:
                txt = "".join(p.get("text", "") for p in r.json()["candidates"][0]["content"]["parts"])
            except Exception as e:
                print("응답 이상", e, r.text[:500]); continue
            open(f"{out}/{fn}", "w", encoding="utf-8").write(txt)
            done = True
            continue
        print(r.text[:300]); time.sleep(60)
