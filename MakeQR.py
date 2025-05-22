import qrcode


link="http://www.ncam.kr/" #원하는 (인터넷)링크 기입
save_path="D:/py/qrcode/NCAM.png" #원하는 저장경로 기입

qr=qrcode.make(link)
qr.save(save_path)
