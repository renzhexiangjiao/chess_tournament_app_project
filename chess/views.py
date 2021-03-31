from django.shortcuts import render
from django.views import View
from chess.models import Tournament, Game

class IndexView(View):
    def get(self, request):
        return render(request, 'chess/index.html')
        
def show_tournament_history(request):
    context_dict = {}
    
    try:
        tournaments = Tournament.objects.all()
        
        context_dict['tournaments'] = tournaments
    except Tournament.DoesNotExist:
        context_dict['tournaments'] = None
    
    return render(request, 'chess/tournament_history.html', context=context_dict)

def show_tournament(request, tournament_name):
    context_dict = {}
    
    try:
        tournament = Tournament.objects.get(name=tournament_name)
        games = Game.objects.filter(tournament=tournament)
        
        context_dict['games'] = games
        context_dict['tournament'] = tournament
    except Category.DoesNotExist:
        context_dict['games'] = None
        context_dict['tournament'] = None
    
    return render(request, 'chess/tournament.html', context=context_dict)

def show_calendar(request):
    return render(request, 'chess/calendar.html')