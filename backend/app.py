# backend/app.py
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from controllers.auth import auth_bp
from controllers.meeting import meeting_bp
from controllers.todo import todo_bp
from models import db
import config

app = Flask(__name__)
app.config.from_object(config.Config)

# Configure CORS
CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

# Initialize database
db.init_app(app)

# Initialize JWT
jwt = JWTManager(app)

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(meeting_bp, url_prefix='/api/meetings')
app.register_blueprint(todo_bp, url_prefix='/api/todos')

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "message": "MeetNote API is running"})

@app.before_request
def create_tables():
    with app.app_context():
        db.create_all()
        
@app.errorhandler(422)
def handle_unprocessable_entity(error):
    return jsonify({"error": "Invalid JWT token or token is missing"}), 422

@app.errorhandler(404)
def handle_not_found(error):
    return jsonify({"error": "Resource not found"}), 404

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'], host='0.0.0.0', port=5000)