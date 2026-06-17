from qr_logic import generate_qr, decode_qr

def string_to_qr():

    text =input("Enter text to convert into QR code : ")

    filename =input("Enter filename to save the QR code(no extension needed) : ")
    if not filename:    
        filename ="qr_code"
    
    filepath = generate_qr(text, filename)
    print("!!! QR code genertaed and saved as", filepath, "!!!")


def qr_to_string():
    filename = input("Enter file-name of thr QR code tto decode(with extension) : ")
    try:
        text = decode_qr(filename)
        print("QR decoded succesfully:")
        print(f"Data : {text}")
    except FileNotFoundError as e:
        print(f"!!! Error: {e}")
    except ValueError as e:
        print(f"!!! Error: {e}")
    except Exception as e:
        print(f"!!! Error reading image: {e}")

def main():
    print("*" * 50 )
    print("QR CODE GENERATOR AND DECODER")
    print("*" * 50 )
    print("\n MENU")
    print("1. Text-to-QR code")
    print("2. QR-to-Text")
    print("3. EXIT")

    while True:
        choice = int(input("Enter your choice : "))
        if choice ==1:
            string_to_qr()
        elif choice==2:
            qr_to_string()
        elif choice ==3:
            print("!!!Exiting the program, Goodbye.")
            break
        else:
            print("!!! Invalid choice, pls enter valid choice (1, 2 or 3)")
        

if __name__ == "__main__":
    main()
