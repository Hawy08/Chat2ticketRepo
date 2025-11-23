from googleapiclient.discovery import build
from email.mime.text import MIMEText
import base64

def create_calendar_event(creds, event_details):
    """Creates a Google Calendar event."""
    service = build('calendar', 'v3', credentials=creds)

    event = {
        'summary': event_details['name'],
        'location': event_details['location'],
        'description': event_details['description'],
        'start': {
            'dateTime': f"{event_details['date']}T{event_details['time']}",
            'timeZone': 'UTC', # Ideally, get this from the event or user
        },
        'end': {
            'dateTime': f"{event_details['date']}T{event_details['time']}", # Assuming 1 hour duration for simplicity if end time missing
            'timeZone': 'UTC',
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
            ],
        },
    }

    # Adjust end time to be 2 hours later by default
    # Note: A robust implementation would handle datetime parsing more carefully
    # For now, we rely on the string format being ISO-like or compatible
    
    try:
        event = service.events().insert(calendarId='primary', body=event).execute()
        print(f"Event created: {event.get('htmlLink')}")
        return event
    except Exception as e:
        print(f"An error occurred creating calendar event: {e}")
        return None

def send_confirmation_email(creds, to_email, event_details):
    """Sends a confirmation email via Gmail."""
    service = build('gmail', 'v1', credentials=creds)

    message_text = f"""
    Hi there,

    Your booking for {event_details['name']} is confirmed!
    
    Date: {event_details['date']}
    Time: {event_details['time']}
    Location: {event_details['location']}
    
    We have also added this to your Google Calendar.
    
    Enjoy the event!
    """

    message = MIMEText(message_text)
    message['to'] = to_email
    message['subject'] = f"Booking Confirmed: {event_details['name']}"
    
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
    body = {'raw': raw_message}

    try:
        message = service.users().messages().send(userId='me', body=body).execute()
        print(f"Message Id: {message['id']}")
        return message
    except Exception as e:
        print(f"An error occurred sending email: {e}")
        return None

def send_email(creds, to_email, subject, body_text):
    """Sends a generic email via Gmail."""
    service = build('gmail', 'v1', credentials=creds)

    message = MIMEText(body_text)
    message['to'] = to_email
    message['subject'] = subject
    
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
    body = {'raw': raw_message}

    try:
        message = service.users().messages().send(userId='me', body=body).execute()
        print(f"Message Id: {message['id']}")
        return message
    except Exception as e:
        print(f"An error occurred sending email: {e}")
        return None
