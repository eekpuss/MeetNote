# backend/app.py
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from controllers.auth import auth_bp
from controllers.meeting import meeting_bp
from controllers.todo import todo_bp
from models import db
from config import Config
import os

# Inisialisasi aplikasi Flask
app = Flask(__name__, static_url_path='', static_folder='../frontend')
app.config.from_object(Config)

# Konfigurasi CORS
CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

# Inisialisasi database
db.init_app(app)

# Inisialisasi JWT
jwt = JWTManager(app)

# Register blueprints API
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(meeting_bp, url_prefix='/api/meetings')
app.register_blueprint(todo_bp, url_prefix='/api/todos')

# Route untuk health check API
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "message": "MeetNote API is running"})

# Route untuk halaman root/index dengan redirect ke frontend
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

# Route untuk semua file static frontend
@app.route('/<path:path>')
def serve_frontend(path):
    if path.startswith('api/'):
        # Jika path dimulai dengan 'api/', biarkan routes API menanganinya
        return {"error": "API endpoint not found"}, 404
    
    if os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        # Jika file tidak ditemukan, kembalikan index.html untuk SPA routing
        return send_from_directory(app.static_folder, 'index.html')

# Handler error 422 (Invalid token JWT)
@app.errorhandler(422)
def handle_unprocessable_entity(error):
    return jsonify({"error": "Invalid JWT token or token is missing"}), 422

# Handler error 404 (Not Found)
@app.errorhandler(404)
def handle_not_found(error):
    # Jika request ke API, kembalikan JSON error
    if request.path.startswith('/api/'):
        return jsonify({"error": "Resource not found"}), 404
    # Jika request ke frontend, kembalikan halaman index.html
    return send_from_directory(app.static_folder, 'index.html')

# Buat tabel database sebelum request pertama
@app.before_request
def create_tables():
    with app.app_context():
        db.create_all()

# Jalankan aplikasi
if __name__ == '__main__':
    # Pastikan database directory ada
    os.makedirs('database', exist_ok=True)
    
    # Jalankan aplikasi dalam mode debug
    app.run(debug=True, host='0.0.0.0', port=5000)