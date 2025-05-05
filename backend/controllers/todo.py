# backend/controllers/todo.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db
from models.todo import Todo
from models.user import User
from datetime import datetime
from utils.email import send_todo_notification

todo_bp = Blueprint('todo', __name__)

@todo_bp.route('/', methods=['POST'])
@jwt_required()
def create_todo():
    data = request.get_json()
    current_user_id = get_jwt_identity()
    
    # Create new todo
    new_todo = Todo(
        title=data['title'],
        description=data.get('description', ''),
        priority=data.get('priority', 'medium'),
        creator_id=current_user_id,
        meeting_id=data.get('meeting_id')
    )
    
    # Set deadline if provided
    if 'deadline' in data and data['deadline']:
        new_todo.deadline = datetime.fromisoformat(data['deadline'])
    
    # Set assignee if provided
    if 'assignee_id' in data and data['assignee_id']:
        new_todo.assignee_id = data['assignee_id']
        
        # Send notification to assignee
        assignee = User.query.get(data['assignee_id'])
        if assignee and assignee.id != current_user_id:
            send_todo_notification(assignee.email, new_todo)
    
    db.session.add(new_todo)
    db.session.commit()
    
    return jsonify(new_todo.to_dict()), 201

@todo_bp.route('/', methods=['GET'])
@jwt_required()
def get_todos():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    # Get query parameters
    status = request.args.get('status')
    priority = request.args.get('priority')
    meeting_id = request.args.get('meeting_id')
    assignee_id = request.args.get('assignee_id')
    
    # Base query
    if user.is_admin:
        query = Todo.query
    else:
        # User can see todos they created or are assigned to
        query = Todo.query.filter((Todo.creator_id == current_user_id) | 
                                   (Todo.assignee_id == current_user_id))
    
    # Apply filters if provided
    if status:
        query = query.filter(Todo.status == status)
    if priority:
        query = query.filter(Todo.priority == priority)
    if meeting_id:
        query = query.filter(Todo.meeting_id == meeting_id)
    if assignee_id:
        query = query.filter(Todo.assignee_id == assignee_id)
    
    # Sort by deadline
    todos = query.order_by(Todo.deadline).all()
    
    return jsonify([todo.to_dict() for todo in todos]), 200

@todo_bp.route('/<int:todo_id>', methods=['GET'])
@jwt_required()
def get_todo(todo_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    todo = Todo.query.get(todo_id)
    
    if not todo:
        return jsonify({"error": "Todo not found"}), 404
    
    # Check if user is admin, creator or assignee
    if not user.is_admin and current_user_id != todo.creator_id and current_user_id != todo.assignee_id:
        return jsonify({"error": "Unauthorized access"}), 403
    
    return jsonify(todo.to_dict()), 200

@todo_bp.route('/<int:todo_id>', methods=['PUT'])
@jwt_required()
def update_todo(todo_id):
    data = request.get_json()
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    todo = Todo.query.get(todo_id)
    
    if not todo:
        return jsonify({"error": "Todo not found"}), 404
    
    # Check if user is admin, creator or assignee
    if not user.is_admin and current_user_id != todo.creator_id and current_user_id != todo.assignee_id:
        return jsonify({"error": "Unauthorized access"}), 403
    
    # Only admin and creator can update most fields
    if user.is_admin or current_user_id == todo.creator_id:
        todo.title = data.get('title', todo.title)
        todo.description = data.get('description', todo.description)
        todo.priority = data.get('priority', todo.priority)
        
        # Update deadline if provided
        if 'deadline' in data:
            todo.deadline = datetime.fromisoformat(data['deadline']) if data['deadline'] else None
        
        # Update assignee if provided
        if 'assignee_id' in data and data['assignee_id'] != todo.assignee_id:
            old_assignee_id = todo.assignee_id
            todo.assignee_id = data['assignee_id']
            
            # Send notification to new assignee
            if todo.assignee_id:
                assignee = User.query.get(todo.assignee_id)
                if assignee and assignee.id != current_user_id:
                    send_todo_notification(assignee.email, todo)
    
    # Anyone assigned can update status
    if 'status' in data:
        todo.status = data['status']
    
    db.session.commit()
    
    return jsonify(todo.to_dict()), 200

@todo_bp.route('/<int:todo_id>', methods=['DELETE'])
@jwt_required()
def delete_todo(todo_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    todo = Todo.query.get(todo_id)
    
    if not todo:
        return jsonify({"error": "Todo not found"}), 404
    
    # Only admin and creator can delete
    if not user.is_admin and current_user_id != todo.creator_id:
        return jsonify({"error": "Unauthorized access"}), 403
    
    db.session.delete(todo)
    db.session.commit()
    
    return jsonify({"message": "Todo deleted successfully"}), 200