from django.shortcuts import render
from .models import Match
# Create your views here.

def index(request):
    match= Match.objects.all()
    return render(request, 'bolao/index.html', {'match':match})
def bolao(request):
    return render(request, 'bolao/jogos.html',{})