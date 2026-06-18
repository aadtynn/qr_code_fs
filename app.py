from flask import Flask, request, jsonify, send_file
from flask_cors import CORS 
from qr_logic import generate_qr_bytes, decode_qr_bytes

app = Flask(__name__)
CORS(app)
 
@app.route('/api/generate', methods=['POST'])
def generate():
    data = request.get_json()
    
    if not data or 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400
    
    text = data['text']

    if not text.strip():
        return jsonify({'error': 'Text cannot be empty'}), 400
    
    try:
        img_buffer = generate_qr_bytes(text)
        return send_file(
            img_buffer, 
            mimetype='image/png',
            as_attachment=True,
            download_name='qr_code.png'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/api/decode', methods=['POST'])
def decode():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    try:
        file_bytes = file.read()
        text = decode_qr_bytes(file_bytes)
        return jsonify({
            'data': text, 
            'type': 'QRCODE'
        })
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
if __name__ == '__main__':
    app.run(debug=True)