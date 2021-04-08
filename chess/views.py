from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.views import View
from . import gamerules
from chess.models import Tournament, Game, Move, AccountPage
from chess.forms import AccountPageForm
from django.contrib.auth.decorators import login_required
from copy import deepcopy

class IndexView(View):
    def get(self, request):
        return render(request, 'chess/index.html')

class PlayView(View):
    def get(self, request, game_id):
        try:
            game = Game.objects.get(id=game_id)
            spectate_mode = 'spectate' in request.path.split('/')

            perspective = 0
            if not spectate_mode:
                if request.user.is_authenticated and request.user == game.player_white:
                    perspective = 0
                elif request.user.is_authenticated and request.user == game.player_black:
                    perspective = 1
                else:
                    # user does not participate in this game
                    return redirect(reverse('chess:spectate', kwargs={'game_id':game_id}))

            board_state = deepcopy(gamerules.starting_board_state)
            moves = Move.objects.filter(game=game).order_by('move_id')
            for move in moves:
                gamerules.make_move(board_state, move.square_from, move.square_to)

            context_dict = {'perspective': perspective, 'board_state': board_state, 'moves': [move.square_from + move.square_to for move in moves], 'spectate_mode': spectate_mode}
            return render(request, 'chess/play.html', context_dict)
        except Game.DoesNotExist:
            return redirect(reverse('chess:index'))

class PlayLobbyView(View):
    def get(self, request):
        games = Game.objects.all()
        return render(request, 'chess/playlobby.html', { 'games': games })

class MoveListView(View):
    def get(self, request, game_id):
        try:
            game = Game.objects.get(id=game_id)
            board_state = deepcopy(gamerules.starting_board_state)

            # execute moves on the board in order
            moves = Move.objects.filter(game=game).order_by('move_id')
            for move in moves:
                gamerules.make_move(board_state, move.square_from, move.square_to)

            # board_state['turn'] is 0 when it's white player's turn, 1 otherwise
            turn = '1' if board_state['turn']==int(request.user==game.player_black) else '0'
            
            move_str = request.GET['move']
            if move_str and (move_str in gamerules.legal_moves(board_state)): # double checks if the received move is valid
                # create a new move in db
                move = Move()
                move.game = game
                move.square_from = move_str[:2]
                move.square_to = move_str[2:]
                move.captured_piece = gamerules.get_piece_at(board_state, move_str[2:])
                move.save()
                # update the board 
                gamerules.make_move(board_state, move.square_from, move.square_to)
                # now is the turn of the opponent
                turn = '0'
            
            return HttpResponse(' '.join([turn] + gamerules.legal_moves(board_state)))
        except Game.DoesNotExist:
            return HttpResponse('')

class MoveUpdateView(View):
    def get(self, request, game_id):
        try:
            game = Game.objects.get(id=game_id)
            moves = Move.objects.filter(game=game).order_by('-move_id')
            if moves:
                # returns the latest move in the game
                return HttpResponse(moves[0].square_from + moves[0].square_to)
            else:
                return HttpResponse('')
        except Game.DoesNotExist:
            return HttpResponse('')
            
        
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
