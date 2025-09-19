# contests/admin.py
from django.contrib import admin
from .models import Event, Trial, Competitor, Submission, Vote

admin.site.register(Event)
admin.site.register(Trial)
admin.site.register(Competitor)
admin.site.register(Submission)
admin.site.register(Vote)