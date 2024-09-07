from PIL import Image
from qrcode.main import QRCode


def generate_qr_code_image(data: str) -> Image.Image:
    qr = QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill="black", back_color="white")
    return img
