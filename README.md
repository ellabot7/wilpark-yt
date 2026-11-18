# wilpark-yt

유튜브 영상 한 편의 자막과 장면 캡처를 받는 작업 창고 (공개 창고라 GitHub 작업 시간 무료).

- 실행: Actions → **grab** → Run workflow → 영상 ID 또는 주소
- 결과: `results` 가지 `{영상ID}/` — `full/` 장면 원본 PNG(파일 이름 = 영상 속 시각), `sheets/` 20장 모음판, `transcript.txt`, `meta.json`, `index.json`
- 비밀값 `YT_COOKIES`: 유튜브 로그인 cookies.txt (부계정 권장)

## 🧵 스레드 요약 → 텔레그램 (threads)

kiwoom-auto-trader 의 GitHub 작업 시간이 막혀서 여기서 대신 돌림. 앱 🧵 버튼은 그대로 쓰면 되고, 이 창고가 10분마다 새 요청을 보고 요약을 보냄.
코드는 비공개 창고에서 그때그때 받아 쓰고(여기 공개되지 않음), 요약·보낸 글 기록도 그쪽 app-data 에 씀. 실행 기록에는 요약 내용을 찍지 않음.

비밀값(Settings → Secrets and variables → Actions): `KIWOOM_TOKEN`(kiwoom-auto-trader Contents 읽기·쓰기 토큰), `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`, `GEMINI_API_KEY`(이미 있음), `THREADS_COOKIES`(있으면).

## 🎬 유튜브 자동 요약 → 텔레그램 (ytsum)

10분마다 앱 🎬 유튜브 요약 화면에 넣은 주소와 윌팍 채널 새 영상을 Gemini 로 요약해 kiwoom-auto-trader app-data(`digest/yt_summary/`)에 저장하고 텔레그램으로 알림. 비밀값은 threads 와 같음. 지금 바로: Actions → ytsum → Run workflow.

## 📨 나스닥선물 사금·황금선 알림 → 텔레그램 (nqline)

장 열린 동안(뉴욕 일 18:00 ~ 금 17:00) 1분마다 야후 NQ=F 1분봉을 보고 🟫 사금 · 🟨 황금선에 닿으면, 그리고 240선 아래 장에서 황금선을 1틱 넘게 뚫으면(▲ 돌파) 텔레그램 한 줄. 선 근처에서 왔다갔다할 때 계속 오지 않게 선마다 처음 한 번 → 전날 폭의 1/4 넘게 멀어졌다가 다시 닿을 때만(앞 알림에서 30분 · 하루 3번까지). 야후 시세가 약 10분 늦어 알림도 그만큼 늦음. 작업 하나가 5시간 반 지켜보고 다음 작업을 불러 이어감. 켜기·끄기: 앱 📈 지수 차트 › 나스닥 선물 분봉 아래 · 📱 라이트 ☰. 시험: Actions → nqline → Run workflow → dry 체크. 비밀값은 dipalert 와 같음.
