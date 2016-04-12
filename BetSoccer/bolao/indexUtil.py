from .models import MatchRegistration,MatchResult,User,Bet,Ranking,RegisterBet
from django.db.models import F
from .messages import  Messages

class IndexUtil:
    matchResult= MatchResult.objects.all()
    matchRegistration= MatchRegistration.objects.all()
    messageLogin = Messages()
    count = 0

    def __init__(self):
        pass
    def betWinRight(self):
        for match in self.matchResult:
            try:
                betWinner = Bet.objects.filter(homeScore = match.homeScore,visitorScore = match.visitorScore,game = match.game)
                betWinnerCount = len(betWinner)
                if(betWinnerCount !=0):
                    for x in betWinner:
                        cred = User.objects.get(id = x.userBets.id)
                        cred.credits = cred.credits + (x.game.amountOfCredits / betWinnerCount)
                        cred.save()
                        Bet.objects.filter(game = x.game).delete()
                    zero = MatchRegistration.objects.get(id = match.game.id)
                    zero.amountOfCredits = 0
                    zero.save()
            except betWinner.DoesNotExist:
                pass

    def betWinOther(self):
        for match in self.matchResult:
            if match.homeScore > match.visitorScore:
                count = count +1
                try:
                    betHomeWin = Bet.objects.filter(homeScore__gt=F('visitorScore'), game = match.game )
                    betHomeWinCount = len(betHomeWin)
                    if(betHomeWinCount !=0):
                        for u in betHomeWin:
                            cred = User.objects.get(id = u.userBets.id)
                            cred.credits = cred.credits + (u.game.amountOfCredits / betHomeWinCount)
                            cred.save()
                            Bet.objects.filter(game = u.game).delete()
                        zero = MatchRegistration.objects.get(id = match.game.id)
                        zero.amountOfCredits = 0
                        zero.save()
                except betHomeWin.DoesNotExist:
                    pass

            elif match.homeScore < match.visitorScore:
                count = count +1
                try:
                    betVisitorWin = Bet.objects.filter(homeScore__lt=F('visitorScore'), game = match.game)
                    betVisitorWinCount = len(betVisitorWin)
                    if(betVisitorWinCount !=0):
                        for u in betVisitorWin:
                            cred = User.objects.get(id = u.userBets.id)
                            cred.credits = cred.credits + (u.game.amountOfCredits / betVisitorWinCount)
                            cred.save()
                            Bet.objects.filter(game = u.game).delete()
                        zero = MatchRegistration.objects.get(id = match.game.id)
                        zero.amountOfCredits = 0
                        zero.save()
                except betVisitorWin.DoesNotExist:
                    pass

            elif match.homeScore == match.visitorScore:
                count = count +1
                try:
                    betDrawWin = Bet.objects.filter(homeScore=F('visitorScore'), game = match.game)
                    betDrawWinCount = len(betDrawWin)
                    if(betDrawWinCount !=0):
                        for u in betDrawWin:
                            cred = User.objects.get(id = u.userBets.id)
                            cred.credits = cred.credits + (u.game.amountOfCredits / betDrawWinCount)
                            cred.save()
                            Bet.objects.filter(game = u.game).delete()
                        zero = MatchRegistration.objects.get(id = match.game.id)
                        zero.amountOfCredits = 0
                        zero.save()
                except betDrawWin.DoesNotExist:
                    pass

            betNone = Bet.objects.filter(game = match.game)
            for n in betNone:
                    cred = User.objects.get(id = n.userBets.id)
                    cred.credits = cred.credits + 5.0
                    cred.save()
                    Bet.objects.filter(game = n.game).delete()
            zero = MatchRegistration.objects.get(id = match.game.id)
            zero.amountOfCredits = 0
            zero.save()
        if self.matchResult.all() ==10:
           delete = matchResult.get().delete()[0]
           delete.save()

