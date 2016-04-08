from django.shortcuts import render
from .models import MatchRegistration,MatchResult,User,Bet,Ranking,RegisterBet
from django.http import HttpResponse
from django.db.models import F

# Create your views here.

def index(request):
    matchResult= MatchResult.objects.all()
    matchRegistration= MatchRegistration.objects.all()
    count = 0
    for match in matchResult:
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
    for match in matchResult:
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
    if matchResult.all() ==10:
       delete = matchResult.get().delete()[0]
       delete.save()

    return render(request, 'bolao/index.html', {'matchResult':matchResult,'matchRegistration':matchRegistration})
def login(request):
    user = request.POST.get("username", "")
    password = request.POST.get("password", "")
    users = User.objects.all()
    ranking = Ranking.objects.all()
    matchRegistration= MatchRegistration.objects.all()
    ordered = users.order_by('-credits')
    registerBet = RegisterBet.objects.all()
    Ranking.objects.all().delete()

    for match in matchRegistration:
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
    for userRnk in ordered:
        try:
            Ranking.objects.get(user = userRnk)
        except Ranking.DoesNotExist:
            rank = Ranking(user = userRnk,position = count)
            rank.save()
            ranking.order_by('-user.credits')
            count = count +1

    for _user in users:
        if _user.login==user and _user.password==password:
            credito = _user.credits
            return render(request,'bolao/jogos.html',{'user':user,'credito': credito,'registerBet':registerBet,'ranking':ranking})
    return index(request)

def apostar(request):
    matchRegistration= MatchRegistration.objects.all()
    userCredito =  User.objects.get(login =request.POST.get("user-Credito",""))
    matchID = MatchRegistration.objects.get(id =request.POST.get("match-id",""))
    users = User.objects.all()
    ranking = Ranking.objects.all()
    ordered = users.order_by('-credits')
    registerBet = RegisterBet.objects.all()
    Ranking.objects.all().delete()
    try:
        check = Bet.objects.get(userBets = userCredito,game = matchID)

    except Bet.DoesNotExist:
        if userCredito.credits > 0.0 :
            bet = Bet(userBets = userCredito,game = matchID,homeScore = request.POST.get("homeScore"+str(matchID.id),"") , visitorScore = request.POST.get("visitorScore"+str(matchID.id),""))
            bet.save()
            userCredito.credits = userCredito.credits - 5.0
            userCredito.save()
            matchID.amountOfCredits = matchID.amountOfCredits + 5.0
            matchID.save()

    for match in matchRegistration:
        try:
            MatchResult.objects.get(game = match)
        except MatchResult.DoesNotExist:
            register = RegisterBet(id = match.id,homeTeam = match.homeTeam,visitorTeam = match.visitorTeam,date = match.date,hora = match.hora,game = match)
            register.save()
    count = 1
    for userRnk in ordered:
        try:
            Ranking.objects.get(user = userRnk)
        except Ranking.DoesNotExist:
            rank = Ranking(user = userRnk,position = count)
            rank.save()
            ranking.order_by('-user.credits')
            count = count +1

    return render( request,'bolao/jogos.html', {'user':userCredito.login,'credito': userCredito.credits,'registerBet':registerBet,'ranking':ranking} )