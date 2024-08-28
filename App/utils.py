from django.contrib.sessions.models import Session
from django.utils import timezone
import json

def is_user_online(user_id):
    sessions = Session.objects.filter(expire_date__gte = timezone.now()) 
    if sessions.exists():
        for session in sessions:
            session_data = json.loads(session.session_data)
            if session_data.get('user_id') == user_id:
                return True
            else:
               False