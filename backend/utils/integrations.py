# backend/utils/integrations.py
import requests
from flask import current_app
import icalendar
from datetime import datetime
from models.meeting import Meeting
from models.user import User
from models import db

def sync_with_google_calendar(meeting, api_key):
    """Sync meeting to Google Calendar"""
    # Implementation would require OAuth setup and Google Calendar API
    # This is a placeholder for the integration
    pass

def create_ical_event(meeting):
    """Create an iCalendar event for a meeting"""
    cal = icalendar.Calendar()
    cal.add('prodid', '-//MeetNote//meetnote.app//')
    cal.add('version', '2.0')
    
    event = icalendar.Event()
    event.add('summary', meeting.title)
    event.add('description', meeting.description)
    event.add('location', meeting.location)
    
    # Add start and end time (assuming 1 hour meetings by default)
    event.add('dtstart', meeting.meeting_date)
    event.add('dtend', meeting.meeting_date.replace(hour=meeting.meeting_date.hour + 1))
    
    # Add organizer
    organizer = User.query.get(meeting.creator_id)
    event.add('organizer', f'mailto:{organizer.email}')
    
    # Add participants
    for participant in meeting.participants:
        attendee = icalendar.vCalAddress(f'mailto:{participant.email}')
        attendee.params['cn'] = icalendar.vText(participant.username)
        attendee.params['ROLE'] = icalendar.vText('REQ-PARTICIPANT')
        event.add('attendee', attendee)
    
    cal.add_component(event)
    return cal.to_ical()

def import_from_trello(board_id, api_key, token):
    """Import tasks from Trello board"""
    # Implementation would require Trello API setup
    # This is a placeholder for the integration
    pass

def send_slack_notification(webhook_url, message):
    """Send notification to Slack channel"""
    payload = {
        "text": message
    }
    
    response = requests.post(webhook_url, json=payload)
    return response.status_code == 200