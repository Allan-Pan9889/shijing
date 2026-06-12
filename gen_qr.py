import qrcode
from qrcode.constants import ERROR_CORRECT_H
from PIL import Image
import os

os.chdir('/Users/a1/cidi-cengyou')
URL = "https://allan-pan9889.github.io/shijing/"

PAPER = (244, 239, 228)
RED   = (158, 75, 63)

qr = qrcode.QRCode(version=None, error_correction=ERROR_CORRECT_H,
                   box_size=20, border=2)
qr.add_data(URL)
qr.make(fit=True)
img = qr.make_image(fill_color=RED, back_color=PAPER).convert("RGB")

# 中心嵌入 logo(复用 512 图标,缩成 ~22% 宽,高容错可承受)
W, H = img.size
logo = Image.open('icons/icon-512.png').convert("RGB")
ls = int(W * 0.22)
logo = logo.resize((ls, ls), Image.LANCZOS)
# logo 周围留白底，避免压住定位
pad = int(ls * 0.12)
plate = Image.new("RGB", (ls + pad*2, ls + pad*2), PAPER)
plate.paste(logo, (pad, pad))
px = (W - plate.width)//2
py = (H - plate.height)//2
img.paste(plate, (px, py))

img.save('qr-shijing.png')
print("二维码已保存 qr-shijing.png", img.size, os.path.getsize('qr-shijing.png'), "bytes")
print("URL:", URL)
