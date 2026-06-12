from PIL import Image, ImageDraw, ImageFont
import os

os.chdir('/Users/a1/cidi-cengyou')
os.makedirs('icons', exist_ok=True)

# 颜色：宣纸底 + 印章红字（与 app 主题 --red:#9e4b3f / --paper:#f4efe4 一致）
PAPER = (244, 239, 228)
RED   = (158, 75, 63)
INK   = (43, 38, 32)

def find_font(size):
    for p in [
        "/System/Library/Fonts/Supplemental/Songti.ttc",
        "/System/Library/Fonts/STSong.ttf",
        "/System/Library/Fonts/Supplemental/Songti.ttf",
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/Hiragino Sans GB.ttc",
    ]:
        if os.path.exists(p):
            try: return ImageFont.truetype(p, size)
            except: pass
    return ImageFont.load_default()

def make_icon(size, fname):
    img = Image.new("RGB", (size, size), PAPER)
    d = ImageDraw.Draw(img)
    # 外圈印章红边框
    m = int(size*0.08)
    bw = max(2, int(size*0.025))
    d.rounded_rectangle([m, m, size-m, size-m], radius=int(size*0.14),
                        outline=RED, width=bw)
    # 竖排"诗径"两字，居中
    f = find_font(int(size*0.42))
    chars = ["诗", "径"]
    # 计算总高
    hs = []
    for ch in chars:
        bbox = d.textbbox((0,0), ch, font=f)
        hs.append(bbox[3]-bbox[1])
    gap = int(size*0.04)
    total_h = sum(hs) + gap*(len(chars)-1)
    y = (size - total_h)//2
    for i, ch in enumerate(chars):
        bbox = d.textbbox((0,0), ch, font=f)
        w = bbox[2]-bbox[0]
        x = (size - w)//2 - bbox[0]
        d.text((x, y - bbox[1]), ch, fill=RED, font=f)
        y += hs[i] + gap
    img.save(fname, "PNG")
    return fname

for s, n in [(180,'icons/icon-180.png'), (192,'icons/icon-192.png'),
             (512,'icons/icon-512.png')]:
    make_icon(s, n)
    print("生成", n, os.path.getsize(n), "bytes")

# maskable 版（留更大安全边距，给安卓/部分启动器圆形裁切用）
def make_maskable(size, fname):
    img = Image.new("RGB", (size, size), RED)
    d = ImageDraw.Draw(img)
    inner = int(size*0.16)
    d.rounded_rectangle([inner, inner, size-inner, size-inner],
                        radius=int(size*0.08), fill=PAPER)
    f = find_font(int(size*0.30))
    chars=["诗","径"]; hs=[]
    for ch in chars:
        b=d.textbbox((0,0),ch,font=f); hs.append(b[3]-b[1])
    gap=int(size*0.03); th=sum(hs)+gap
    y=(size-th)//2
    for i,ch in enumerate(chars):
        b=d.textbbox((0,0),ch,font=f); w=b[2]-b[0]
        d.text(((size-w)//2-b[0], y-b[1]), ch, fill=RED, font=f)
        y+=hs[i]+gap
    img.save(fname,"PNG")
    return fname
make_maskable(512,'icons/icon-maskable-512.png')
print("生成 icons/icon-maskable-512.png")
print("DONE")
