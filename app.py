import os
import re
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from PIL import UnidentifiedImageError

from qr_logic import generate_qr_bytes, decode_qr_bytes
from models import db, User, QRHistory
from auth import generate_token, token_required

app = Flask(__name__)

app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  
MAX_TEXT_LENGTH = 2000 
MIN_PASSWORD_LENGTH = 8

ALLOWED_MIME_TYPES = {'image/png', 'image/jpeg', 'image/webp', 'image/bmp'}
ALLOWED_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.webp', '.bmp'}
EMAIL_RE = re.compile(r'^[^@\s]+@[^@\s]+\.[^@\s]+$')


app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 'sqlite:///qr_app.db'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()


FRONTEND_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
CORS(app, resources={r"/api/*": {"origins": FRONTEND_ORIGINS}})


@app.errorhandler(413)
def file_too_large(e):
    return jsonify({'error': 'File exceeds the 5MB upload limit'}), 413


@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json(silent=True) or {}
    email = (data.get('email') or '').strip().lower()
    password = data.get('password') or ''

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    if not EMAIL_RE.match(email):
        return jsonify({'error': 'Invalid email address'}), 400

    if len(password) < MIN_PASSWORD_LENGTH:
        return jsonify({'error': f'Password must be at least {MIN_PASSWORD_LENGTH} characters'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'An account with this email already exists'}), 409

    user = User(email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    token = generate_token(user.id)
    return jsonify({'token': token, 'user': user.to_dict()}), 201


@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json(silent=True) or {}
    email = (data.get('email') or '').strip().lower()
    password = data.get('password') or ''

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({'error': 'Invalid email or password'}), 401

    token = generate_token(user.id)
    return jsonify({'token': token, 'user': user.to_dict()}), 200


@app.route('/api/auth/me', methods=['GET'])
@token_required
def me(user_id):
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({'user': user.to_dict()})


@app.route('/api/generate', methods=['POST'])
@token_required
def generate(user_id):
    data = request.get_json(silent=True)

    if not data or 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400

    text = data['text']

    if not text.strip():
        return jsonify({'error': 'Text cannot be empty'}), 400

    if len(text) > MAX_TEXT_LENGTH:
        return jsonify({'error': f'Text exceeds max length of {MAX_TEXT_LENGTH} characters'}), 400

    try:
        img_buffer = generate_qr_bytes(text)

        history_entry = QRHistory(user_id=user_id, action='generate', data=text)
        db.session.add(history_entry)
        db.session.commit()

        return send_file(
            img_buffer,
            mimetype='image/png',
            as_attachment=True,
            download_name='qr_code.png'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/decode', methods=['POST'])
@token_required
def decode(user_id):
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        return jsonify({
            'error': f'Unsupported file extension "{ext}". Allowed: {", ".join(sorted(ALLOWED_EXTENSIONS))}'
        }), 400

    if file.mimetype not in ALLOWED_MIME_TYPES:
        return jsonify({
            'error': f'Unsupported content type "{file.mimetype}". Please upload an image file.'
        }), 400

    try:
        file_bytes = file.read()
        text = decode_qr_bytes(file_bytes)

        history_entry = QRHistory(user_id=user_id, action='decode', data=text)
        db.session.add(history_entry)
        db.session.commit()

        return jsonify({
            'data': text,
            'type': 'QRCODE'
        })
    except UnidentifiedImageError:
        return jsonify({'error': 'File could not be read as an image'}), 400
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/history', methods=['GET'])
@token_required
def history(user_id):
    limit = min(int(request.args.get('limit', 50)), 200)
    entries = (
        QRHistory.query
        .filter_by(user_id=user_id)
        .order_by(QRHistory.created_at.desc())
        .limit(limit)
        .all()
    )
    return jsonify({'history': [e.to_dict() for e in entries]})


@app.route('/api/history/<entry_id>', methods=['DELETE'])
@token_required
def delete_history_entry(user_id, entry_id):
    entry = QRHistory.query.filter_by(id=entry_id, user_id=user_id).first()
    if not entry:
        return jsonify({'error': 'History entry not found'}), 404

    db.session.delete(entry)
    db.session.commit()
    return jsonify({'message': 'Deleted'}), 200


if __name__ == '__main__':
    app.run(debug=True)