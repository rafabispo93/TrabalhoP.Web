from .models import MatchRegistration,MatchResult,User,Bet,Ranking,RegisterBet
from django.db.models import F
from .messages import  Messages


class Aposta:
    cred = None
    id = None

    matchRegistration= MatchRegistration.objects.all()
    userCredito = None
    matchID = None

    users = User.objects.all()
    ranking = Ranking.objects.all()
    ordered = users.order_by('-credits')
    registerBet = RegisterBet.objects.all()


    def __init__(self,cred,id):
        self.cred = cred
        self.id = id
        self.userCredito =  User.objects.get(login =self.cred)
        self.matchID = MatchRegistration.objects.get(id =self.id)



    def apostarRefresh(self):

        for match in self.matchRegistration:
            try:
                MatchResult.objects.get(game = match)
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