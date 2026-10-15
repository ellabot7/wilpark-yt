# 유튜브 자막(vtt) → "분:초 글" 한 줄씩, 자동 자막의 겹치는 줄은 한 번만
import re, sys
out, last = [], ""
t = "0:00"
for line in open(sys.argv[1], encoding="utf-8"):
    line = line.strip()
    m = re.match(r"(\d+):(\d\d):(\d\d)\.\d+ -->", line)
    if m:
        h, mi, se = map(int, m.groups()); t = f"{h * 60 + mi}:{se:02d}"; continue
    if not line or line.startswith(("WEBVTT", "Kind:", "Language:")) or "-->" in line:
        continue
    txt = re.sub(r"<[^>]+>", "", line).strip()
    if txt and txt != last:
        out.append(f"{t} {txt}"); last = txt
open(sys.argv[2], "w", encoding="utf-8").write("\n".join(out))
