import qrcode
from PIL import Image
from pyzbar.pyzbar import decode
import os
import io


def generate_qr(text, filename="qr_code"):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4
    )
    qr.add_data(text)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    filepath = f"{filename}.png"
    img.save(filepath)
    return filepath

def generate_qr_bytes(text):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4
    )
    qr.add_data(text)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer
           
def decode_qr(filepath):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"{filepath} does not exist.")
    
    img = Image.open(filepath)
    decode_objects = decode(img)

    if not decode_objects:
        raise ValueError(f"No QR code found in {filepath}")
    
    return decode_objects[0].data.decode('utf-8')

def decode_qr_bytes(file_bytes):
    img = Image.open(io.BytesIO(file_bytes))
    decode_objects = decode(img)
    if not decode_objects:
        raise ValueError("No QR code found in image.")
    return decode_objects[0].data.decode('utf-8')