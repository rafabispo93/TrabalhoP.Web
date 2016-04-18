from django.contrib import admin
from .models import User,MatchRegistration,MatchResult,RegisterBet,Bet
# Register your models here.

admin.site.register(User)
admin.site.register(MatchResult)
admin.site.register(MatchRegistration)

