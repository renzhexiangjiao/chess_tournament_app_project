from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from . import gamerules
from chess.models import Tournament, Game, AccountPage
from chess.forms import AccountPageForm
from django.contrib.auth.decorators import login_required

class IndexView(View):
    def get(self, request):
        return render(request, 'chess/index.html')
        
class PlayView(View):
    def get(self, request, game_id):
        context_dict = {'perspective': 0, 'board_state': gamerules.starting_board_state, 'moves': []}
        return render(request, 'chess/play.html', context_dict)

class PlayLobbyView(View):
    def get(self, request):
        return render(request, 'chess/playlobby.html')

class MoveListView(View):
    def get(self, request, game_id):
        print(request.GET['move'])
        return HttpResponse(' '.join(gamerules.legal_moves(gamerules.starting_board_state)))

class MoveUpdateView(View):
    def get(self, request, game_id):
        return HttpResponse('e2e4')
        
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
    except Tournament.DoesNotExist:
        context_dict['games'] = None
        context_dict['tournament'] = None
    
    return render(request, 'chess/tournament.html', context=context_dict)

def show_calendar(request):
    return render(request, 'chess/calendar.html')

@login_required
def create_accountpage(request):
    filled = False
    
    if request.method == 'POST':
        accountpage_form = AccountPageForm(request.POST)
        
        if accountpage_form.is_valid():
            
            # Since we need to set the user attribute ourselves,
            # we set commit=False. This delays saving the model
            accountpage = accountpage_form.save(commit=False)
            accountpage.user = request.user
            
            if 'picture' in request.FILES:
                accountpage.picture = request.FILES['picture']
            
            accountpage.save()
            
            filled = True
        else:
            print(accountpage_form.errors)
    else:
        accountpage_form = AccountPageForm()
    
    if filled == True:
        return render(request, 'chess/accountpage.html', context=context_dict)
    else:
        return render(request,
                      'chess/create_accountpage.html',
                      context = {'accountpage_form': accountpage_form, 'filled': filled})

def show_accountpage(request):
    context_dict = {}
    
    try:
        accountpage = AccountPage.objects.get(user=request.user)
        context_dict['accountpage'] = accountpage
    except AccountPage.DoesNotExist:
        context_dict['accountpage'] = None
    
    return render(request, 'chess/accountpage.html', context=context_dict)
