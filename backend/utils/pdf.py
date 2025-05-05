# backend/utils/pdf.py
from flask import render_template_string
import pdfkit
from models.user import User

def generate_meeting_pdf(meeting):
    """Generate a PDF from meeting data"""
    # Get creator and participants info
    creator = User.query.get(meeting.creator_id)
    
    # Create a simple HTML template for the PDF
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>{{ meeting.title }} - Meeting Notes</title>
        <style>
            body { font-family: Arial, sans-serif; }
            h1 { color: #333; }
            .section { margin-bottom: 20px; }
            .label { font-weight: bold; }
            .notes { border: 1px solid #ddd; padding: 10px; }
        </style>
    </head>
    <body>
        <h1>{{ meeting.title }}</h1>
        
        <div class="section">
            <p><span class="label">Date:</span> {{ meeting.meeting_date.strftime('%Y-%m-%d %H:%M') }}</p>
            <p><span class="label">Location:</span> {{ meeting.location }}</p>
            <p><span class="label">Organized by:</span> {{ creator.username }}</p>
        </div>
        
        <div class="section">
            <h2>Description</h2>
            <p>{{ meeting.description }}</p>
        </div>
        
        <div class="section">
            <h2>Participants</h2>
            <ul>
                {% for participant in meeting.participants %}
                <li>{{ participant.username }}</li>
                {% endfor %}
            </ul>
        </div>
        
        <div class="section">
            <h2>Meeting Notes</h2>
            <div class="notes">
                {% if meeting.notes %}
                {{ meeting.notes.content|safe }}
                {% else %}
                <p>No notes available.</p>
                {% endif %}
            </div>
        </div>
        
        <div class="section">
            <h2>Action Items</h2>
            <ul>
                {% for todo in meeting.todos %}
                <li>{{ todo.title }} (Assigned to: {{ todo.assignee.username if todo.assignee else 'Unassigned' }}, 
                    Deadline: {{ todo.deadline.strftime('%Y-%m-%d') if todo.deadline else 'No deadline' }})</li>
                {% endfor %}
            </ul>
        </div>
    </body>
    </html>
    """
    
    # Render the template with data
    html_content = render_template_string(
        html_template, 
        meeting=meeting,
        creator=creator
    )
    
    # Convert HTML to PDF
    pdf = pdfkit.from_string(html_content, False)
    
    return pdf