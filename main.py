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


def qr_to_string():
    filename =input("Enter file-name of the QR code (with extension) : ")

    if not os.path.exists(filename):
        print(f"!!! File not found - {filename} does not exist.")
        return
    
    try:
        img =Image.open(filename)
        decoded_objects =decode(img)

        if not decoded_objects:
            print("!!! No QR found in image.")
            return
        
        print("QR code decoded successfully:")
        for obj in decoded_objects:
            print(f"Type : {obj.type}")
            print(f"Data : {obj.data.decode('utf-8')}")

    except Exception as e:
        print(f"!!!Error reading image: {e}")
        
        

def main():
    print("*" * 50 )
    print("QR CODE GENERATOR AND DECODER")
    print("*" * 50 )
    print("\n MENU")
    print("1. Text-to-QR code")
    print("2. QR-to-Text")
    print("3. EXIT")

    while True:
        ch=int(input("Enter your choice : "))
        if ch ==1:
            string_to_qr()
        elif ch==2:
            qr_to_string()
        elif ch ==3:
            print("!!!Exiting the program, Goodbye.")
            break
        else:
            print("!!! Invalid choice, pls enter valid choice (1, 2 or 3)")
        

if __name__ == "__main__":
    main()
