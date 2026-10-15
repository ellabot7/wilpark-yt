# 영상 전체를 받아 화면이 바뀌는 곳 + 15초마다 프레임을 뽑고, 비슷한 것은 하나만 남김 → out/ 에 원본 PNG, 축소 모음판
import glob, json, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw
vid = sys.argv[1]; out = sys.argv[2]
os.makedirs(out + "/full", exist_ok=True); os.makedirs(out + "/sheets", exist_ok=True)
v = sorted(glob.glob("video.*"))[0]
probe = json.loads(subprocess.check_output(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", v]))
dur = float(probe["format"]["duration"])
# 1) 1초마다 작은 회색 그림(64x36)으로 전체 훑기
raw = subprocess.check_output(["ffmpeg", "-loglevel", "error", "-i", v, "-vf", "fps=1,scale=64:36,format=gray", "-f", "rawvideo", "-"])
a = np.frombuffer(raw, np.uint8).reshape(-1, 36, 64).astype(np.int16)
n = len(a)
# 2) 화면이 안정된 구간마다 대표 1장: 직전 대표와 충분히 다르고, 앞뒤 2초가 거의 같은(멈춘) 장면
keep, last = [], None
for t in range(2, n - 2):
    stable = np.abs(a[t] - a[t - 1]).mean() < 3 and np.abs(a[t + 1] - a[t]).mean() < 3
    if not stable:
        continue
    if last is None or np.abs(a[t] - a[last]).mean() > 6:
        keep.append(t); last = t
    elif t - last > 120 and np.abs(a[t] - a[last]).mean() > 3:
        keep.append(t); last = t
if len(keep) > 400:                                   # 너무 많으면 고르게 400장만
    keep = [keep[int(i * len(keep) / 400)] for i in range(400)]
print("frames", n, "keep", len(keep))
names = []
for t in keep:
    hh, mm, ss = t // 3600, t % 3600 // 60, t % 60
    nm = f"{hh:01d}h{mm:02d}m{ss:02d}s.png"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", str(t), "-i", v, "-frames:v", "1", f"{out}/full/{nm}"], check=True)
    names.append((t, nm))
# 3) 모음판: 한 장에 4x5=20칸, 칸마다 시각 글씨
W, H, C, R = 480, 270, 4, 5
for i in range(0, len(names), C * R):
    sh = Image.new("RGB", (W * C, (H + 22) * R), "white"); d = ImageDraw.Draw(sh)
    for j, (t, nm) in enumerate(names[i:i + C * R]):
        im = Image.open(f"{out}/full/{nm}").convert("RGB").resize((W, H))
        x, y = j % C * W, j // C * (H + 22)
        sh.paste(im, (x, y + 22)); d.text((x + 4, y + 4), f"#{i + j + 1} {nm[:-4]}", fill="black")
    sh.save(f"{out}/sheets/sheet_{i // (C * R) + 1:02d}.jpg", quality=80)
w = [s for s in probe["streams"] if s["codec_type"] == "video"][0]
json.dump(dict(id=vid, duration=dur, width=w["width"], height=w["height"], frames=[dict(t=t, file=nm) for t, nm in names]),
          open(f"{out}/index.json", "w"), ensure_ascii=False, indent=1)
