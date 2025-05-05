# backend/models/user.py
from . import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Hubungan dengan Meeting
    meetings_created = db.relationship('Meeting', backref='creator', lazy='dynamic', 
                                      foreign_keys='Meeting.creator_id')
    
    # Hubungan dengan Todo - Memperbaiki ambiguitas
    todos_assigned = db.relationship('Todo', backref='assignee', lazy='dynamic',
                                   foreign_keys='Todo.assignee_id')
    
    # Tambahkan juga relasi untuk Todo yang dibuat user
    todos_created = db.relationship('Todo', backref='creator', lazy='dynamic',
                                   foreign_keys='Todo.creator_id')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }