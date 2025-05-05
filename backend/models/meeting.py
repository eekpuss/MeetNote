# backend/models/meeting.py
from . import db
from datetime import datetime

# Association table for meeting participants
meeting_participants = db.Table('meeting_participants',
    db.Column('meeting_id', db.Integer, db.ForeignKey('meetings.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('attended', db.Boolean, default=False)
)

class Meeting(db.Model):
    __tablename__ = 'meetings'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text)
    location = db.Column(db.String(128))
    meeting_date = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Relationships
    participants = db.relationship('User', secondary=meeting_participants, 
                                   backref=db.backref('meetings_participated', lazy='dynamic'))
    todos = db.relationship('Todo', backref='meeting', lazy='dynamic')
    notes = db.relationship('MeetingNote', backref='meeting', uselist=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'location': self.location,
            'meeting_date': self.meeting_date.isoformat(),
            'creator_id': self.creator_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'participants': [user.to_dict() for user in self.participants],
            'todos': [todo.to_dict() for todo in self.todos],
            'notes': self.notes.to_dict() if self.notes else None
        }

class MeetingNote(db.Model):
    __tablename__ = 'meeting_notes'
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    meeting_id = db.Column(db.Integer, db.ForeignKey('meetings.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    updated_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    def to_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'meeting_id': self.meeting_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'updated_by': self.updated_by
        }