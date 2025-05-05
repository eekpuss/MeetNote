# backend/controllers/meeting.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db
from models.meeting import Meeting, MeetingNote
from models.user import User
from utils.pdf import generate_meeting_pdf
from utils.email import send_meeting_notification
from datetime import datetime

meeting_bp = Blueprint('meeting', __name__)

@meeting_bp.route('/', methods=['POST'])
@jwt_required()
def create_meeting():
    data = request.get_json()
    current_user_id = get_jwt_identity()
    
    # Create new meeting
    new_meeting = Meeting(
        title=data['title'],
        description=data.get('description', ''),
        location=data.get('location', ''),
        meeting_date=datetime.fromisoformat(data['meeting_date']),
        creator_id=current_user_id
    )
    
    # Add participants
    if 'participant_ids' in data:
        for participant_id in data['participant_ids']:
            user = User.query.get(participant_id)
            if user:
                new_meeting.participants.append(user)
    
    # Add creator as participant
    creator = User.query.get(current_user_id)
    new_meeting.participants.append(creator)
    
    db.session.add(new_meeting)
    db.session.commit()
    
    # Create empty notes for the meeting
    new_note = MeetingNote(
        content='',
        meeting_id=new_meeting.id,
        updated_by=current_user_id
    )
    db.session.add(new_note)
    db.session.commit()
    
    # Send notifications to participants
    for participant in new_meeting.participants:
        if participant.id != current_user_id:
            send_meeting_notification(participant.email, new_meeting)
    
    return jsonify(new_meeting.to_dict()), 201

@meeting_bp.route('/', methods=['GET'])
@jwt_required()
def get_meetings():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    # Get query parameters
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    # Base query
    if user.is_admin:
        query = Meeting.query
    else:
        query = Meeting.query.filter(Meeting.participants.any(id=current_user_id))
    
    # Apply date filters if provided
    if start_date:
        query = query.filter(Meeting.meeting_date >= datetime.fromisoformat(start_date))
    if end_date:
        query = query.filter(Meeting.meeting_date <= datetime.fromisoformat(end_date))
    
    # Sort by meeting date
    meetings = query.order_by(Meeting.meeting_date).all()
    
    return jsonify([meeting.to_dict() for meeting in meetings]), 200

@meeting_bp.route('/<int:meeting_id>', methods=['GET'])
@jwt_required()
def get_meeting(meeting_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    meeting = Meeting.query.get(meeting_id)
    
    if not meeting:
        return jsonify({"error": "Meeting not found"}), 404
    
    # Check if user is admin or participant
    if not user.is_admin and current_user_id not in [p.id for p in meeting.participants]:
        return jsonify({"error": "Unauthorized access"}), 403
    
    return jsonify(meeting.to_dict()), 200

@meeting_bp.route('/<int:meeting_id>', methods=['PUT'])
@jwt_required()
def update_meeting(meeting_id):
    data = request.get_json()
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    meeting = Meeting.query.get(meeting_id)
    
    if not meeting:
        return jsonify({"error": "Meeting not found"}), 404
    
    # Check if user is admin or creator
    if not user.is_admin and meeting.creator_id != current_user_id:
        return jsonify({"error": "Unauthorized access"}), 403
    
    # Update meeting details
    meeting.title = data.get('title', meeting.title)
    meeting.description = data.get('description', meeting.description)
    meeting.location = data.get('location', meeting.location)
    
    if 'meeting_date' in data:
        meeting.meeting_date = datetime.fromisoformat(data['meeting_date'])
    
    # Update participants
    if 'participant_ids' in data:
        # Clear existing participants
        meeting.participants = []
        
        # Add new participants
        for participant_id in data['participant_ids']:
            user = User.query.get(participant_id)
            if user:
                meeting.participants.append(user)
        
        # Ensure creator is still a participant
        creator = User.query.get(meeting.creator_id)
        if creator not in meeting.participants:
            meeting.participants.append(creator)
    
    db.session.commit()
    
    return jsonify(meeting.to_dict()), 200

@meeting_bp.route('/<int:meeting_id>/notes', methods=['PUT'])
@jwt_required()
def update_meeting_notes(meeting_id):
    data = request.get_json()
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    meeting = Meeting.query.get(meeting_id)
    
    if not meeting:
        return jsonify({"error": "Meeting not found"}), 404
    
    # Check if user is admin or participant
    if not user.is_admin and current_user_id not in [p.id for p in meeting.participants]:
        return jsonify({"error": "Unauthorized access"}), 403
    
    # Update notes
    if meeting.notes:
        meeting.notes.content = data['content']
        meeting.notes.updated_by = current_user_id
    else:
        new_note = MeetingNote(
            content=data['content'],
            meeting_id=meeting_id,
            updated_by=current_user_id
        )
        db.session.add(new_note)
    
    db.session.commit()
    
    return jsonify(meeting.notes.to_dict()), 200

@meeting_bp.route('/<int:meeting_id>/export', methods=['GET'])
@jwt_required()
def export_meeting_pdf(meeting_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    meeting = Meeting.query.get(meeting_id)
    
    if not meeting:
        return jsonify({"error": "Meeting not found"}), 404
    
    # Check if user is admin or participant
    if not user.is_admin and current_user_id not in [p.id for p in meeting.participants]:
        return jsonify({"error": "Unauthorized access"}), 403
    
    pdf_data = generate_meeting_pdf(meeting)
    
    return pdf_data, 200, {
        'Content-Type': 'application/pdf',
        'Content-Disposition': f'attachment; filename=meeting_{meeting_id}.pdf'
    }