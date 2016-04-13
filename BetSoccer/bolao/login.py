from .models import MatchRegistration,MatchResult,User,Bet,Ranking,RegisterBet
from django.db.models import F
from .messages import  Messages

class Login:
    user = None
    passw = None

    users = User.objects.all()
    ranking = Ranking.objects.all()
    matchRegistration= MatchRegistration.objects.all()
    ordered = users.order_by('-credits')
    registerBet = RegisterBet.objects.all()
    credito = None


    def __init__(self,user,passw):
        self.user = user
        self.passw = passw


    def organizeLogin(self):
        Ranking.objects.all().delete()
        for match in self.matchRegistration:
            try:
                MatchResult.objects.get(game = match)
                try:
                    RegisterBet.objects.get(game = match).delete()
                except RegisterBet.DoesNotExist:
                    print()
            except MatchResult.DoesNotExist:
                register = RegisterBet(id = match.id,homeTeam = match.homeTeam,visitorTeam = match.visitorTeam,date = match.date,hora = match.hora,game = match)
                register.save()

        count = 1
        for userRnk in self.ordered:
            try:
                Ranking.objects.get(user = userRnk)
            except Ranking.DoesNotExist:
                rank = Ranking(user = userRnk,position = count)
                rank.save()
                self.ranking.order_by('-user.credits')
                count = count +1
        for _user in self.users:

            if _user.login==self.user and _user.password==self.passw:
                self.credito = _user.credits
                return 1
        return 2
