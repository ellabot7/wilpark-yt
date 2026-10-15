# wilpark-yt

유튜브 영상 한 편의 자막과 장면 캡처를 받는 작업 창고 (공개 창고라 GitHub 작업 시간 무료).

- 실행: Actions → **grab** → Run workflow → 영상 ID 또는 주소
- 결과: `results` 가지 `{영상ID}/` — `full/` 장면 원본 PNG(파일 이름 = 영상 속 시각), `sheets/` 20장 모음판, `transcript.txt`, `meta.json`, `index.json`
- 비밀값 `YT_COOKIES`: 유튜브 로그인 cookies.txt (부계정 권장)
