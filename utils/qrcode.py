from qrcode.main import QRCode
from io import BytesIO
import qrcode


# QR-kod yaratish
def create_qrcode(data):
    qr = QRCode(version=1, box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")
    output = BytesIO()
    qr_img.save(output, format="PNG")
    output.seek(0)
    return output
