import qrcode
from PIL import Image
from pyzbar.pyzbar import decode
import os

def string_to_qr():

    text =input("Enter text to convert into QR code : ")

    filename =input("Enter filename to save the QR code(no extension needed) : ")
    if not filename:    
        filename ="qr_code"
    
    qr =qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4
    )

    qr.add_data(text)
    qr.make(fit=True)

    img =qr.make_image(fill_color="balck", back_color="white")

    filepath =f"{filename}.png"
    img.save(filepath)
    print("!!! QR code generated and saved as", filepath, "!!!")
    





def main():
    print("*" * 50 )
    print("qr code generator")
    print("*" * 50 )
    print("\n MENU")
    print("1. Text-to-QR code")
    print("2. QR-to-Text")
    print("3. EXIT")

    while True:
        ch=int(input("Enter your choice : "))
