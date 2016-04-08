from django.contrib import admin
from .models import User,MatchRegistration,MatchResult,Bet
# Register your models here.

admin.site.register(User)
admin.site.register(MatchResult)
admin.site.register(MatchRegistration)
admin.site.register(Bet)