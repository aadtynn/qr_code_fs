# QR Code Generator & Decoder

A full-stack application for generating and decoding QR codes, built as a learning project to demonstrate full-stack development skills.

## 🚀 Features

### Phase 1: CLI Tool ✅
- Generate QR codes from text input
- Decode QR codes from image files
- Save QR codes as PNG files
- Interactive command-line menu
- Error handling for missing files and invalid QR codes

### Phase 2: Web Application (Coming Soon)
- Django/Flask REST API backend
- React frontend with modern UI
- User authentication
- QR code history and management

## 🛠️ Tech Stack

- **Backend:** Python 3.12
- **Frontend:** React (coming soon)
- **Libraries:** qrcode, pyzbar, Pillow

## 📖 How to Run

### Prerequisites
- Python 3.12+
- pip

### Installation

1. Clone the repository:
```bash
git clone https://github.com/aadtynn/qr_code_fs.git
cd qr_code_fs
```

2. Create and activate virtual environment:
```bash
# Create virtual environment
python3 -m venv qrcodeproject

# Activate it
# On Linux/Mac with bash/zsh:
source qrcodeproject/bin/activate

# On Linux/Mac with fish shell:
source qrcodeproject/bin/activate.fish

# On Windows:
qrcodeproject\Scripts\activate
```

3. Install system dependencies (Linux only):
```bash
sudo apt-get install libzbar0
```

4. Install Python dependencies:
```bash
pip install -r requirements.txt
```

5. Run the CLI tool:
```bash
python main.py
```

### Usage

**Generate QR Code:**
1. Select option 1 from the menu
2. Enter your text to encode
3. Enter desired filename (without .png extension)
4. QR code will be saved in the project directory!

**Decode QR Code:**
1. Select option 2 from the menu
2. Enter the QR code filename (with .png extension)
3. See the decoded text displayed!

**Example:**
```
MENU
1. Text-to-QR code
2. QR-to-Text
3. EXIT
Enter your choice : 1
Enter text to convert into QR code : Hello World
Enter filename to save the QR code(no extension needed) : my_qr
!!! QR code generated and saved as my_qr.png !!!
```

## 🗺️ Roadmap

- [x] CLI tool with QR generation
- [x] CLI tool with QR decoding
- [x] Error handling and input validation
- [x] Flask REST API backend
- [x] /api/generate endpoint
- [x] /api/decode endpoint
- [ ] React frontend
- [ ] User authentication system
- [ ] QR code history dashboard
- [ ] Deploy to production

## 🧪 Testing

- ✅ Generated multiple QR codes successfully
- ✅ Decoded QR codes back to original text
- ✅ Verified with real-world QR scanner (iPhone camera)
- ✅ Error handling tested (missing files, invalid images)

## 📝 License

MIT License - feel free to use for learning!

## 👨‍💻 Author

Aadityan Harindran - [GitHub](https://github.com/aadtynn)

---

**Built as a learning project to demonstrate:**
- Python programming
- Git/GitHub workflow
- Full-stack development concepts
- REST API design (coming soon)
- Modern frontend development (coming soon)
