import qrcode

bot_username = "p33_group2_bot"
start_param = "from_qr_code"

link = f"https://t.me/{bot_username}?start={start_param}"

img = qrcode.make(link)
img.save("tg_bot_qr.png")

print(f"QR code yaratildi. Link: {link}")
