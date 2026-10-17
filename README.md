# wilpark-yt

유튜브 영상 한 편의 자막과 장면 캡처를 받는 작업 창고 (공개 창고라 GitHub 작업 시간 무료).

- 실행: Actions → **grab** → Run workflow → 영상 ID 또는 주소
- 결과: `results` 가지 `{영상ID}/` — `full/` 장면 원본 PNG(파일 이름 = 영상 속 시각), `sheets/` 20장 모음판, `transcript.txt`, `meta.json`, `index.json`
- 비밀값 `YT_COOKIES`: 유튜브 로그인 cookies.txt (부계정 권장)

## 🧵 스레드 요약 → 텔레그램 (threads)

kiwoom-auto-trader 의 GitHub 작업 시간이 막혀서 여기서 대신 돌림. 앱 🧵 버튼은 그대로 쓰면 되고, 이 창고가 10분마다 새 요청을 보고 요약을 보냄.
코드는 비공개 창고에서 그때그때 받아 쓰고(여기 공개되지 않음), 요약·보낸 글 기록도 그쪽 app-data 에 씀. 실행 기록에는 요약 내용을 찍지 않음.

비밀값(Settings → Secrets and variables → Actions): `KIWOOM_TOKEN`(kiwoom-auto-trader Contents 읽기·쓰기 토큰), `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`, `GEMINI_API_KEY`(이미 있음), `THREADS_COOKIES`(있으면).
