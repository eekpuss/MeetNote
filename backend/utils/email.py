# backend/utils/email.py
from flask import current_app
from flask_mail import Mail, Message
from datetime import datetime

mail = Mail()

def send_meeting_notification(recipient_email, meeting):
    """Send meeting invitation or update notification"""
    subject = f"MeetNote: You've been invited to: {meeting.title}"
    
    msg = Message(
        subject=subject,
        recipients=[recipient_email],
        sender=current_app.config['MAIL_DEFAULT_SENDER']
    )
    
    msg.body = f"""
    You have been invited to a meeting:
    
    Title: {meeting.title}
    Date: {meeting.meeting_date.strftime('%Y-%m-%d %H:%M')}
    Location: {meeting.location}
    
    Description:
    {meeting.description}
    
    Please log in to MeetNote to view all details and respond.
    """
    
    mail.send(msg)

def send_todo_notification(recipient_email, todo):
    """Send todo assignment notification"""
    subject = f"MeetNote: Task assigned to you: {todo.title}"
    
    deadline_str = todo.deadline.strftime('%Y-%m-%d') if todo.deadline else "No deadline"
    
    msg = Message(
        subject=subject,
        recipients=[recipient_email],
        sender=current_app.config['MAIL_DEFAULT_SENDER']
    )
    
    msg.body = f"""
    A new task has been assigned to you:
    
    Title: {todo.title}
    Priority: {todo.priority.capitalize()}
    Deadline: {deadline_str}
    
    Description:
    {todo.description}
    
    Please log in to MeetNote to view all details and update the status.
    """
    
    mail.send(msg)

def send_deadline_reminder(recipient_email, todo):
    """Send reminder for approaching deadline"""
    subject = f"MeetNote: Reminder - Task deadline approaching: {todo.title}"
    
    msg = Message(
        subject=subject,
        recipients=[recipient_email],
        sender=current_app.config['MAIL_DEFAULT_SENDER']
    )
    
    days_left = (todo.deadline - datetime.utcnow()).days
    
    msg.body = f"""
    Reminder: You have a task with an approaching deadline:
    
    Title: {todo.title}
    Deadline: {todo.deadline.strftime('%Y-%m-%d')}
    Days remaining: {days_left}
    
    Current status: {todo.status.replace('_', ' ').capitalize()}
    
    Please log in to MeetNote to update the status or request an extension if needed.
    """
    
    mail.send(msg)