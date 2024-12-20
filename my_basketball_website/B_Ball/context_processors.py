#This context processor approach  ensure organizers and any other items
# are globally available in all templates, including navbar.

# your_app_name/context_processors.py

from .models import Organizer

def organizers_context(request):
    organizers = Organizer.objects.all()
    return {'organizers': organizers}
