from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.views import View
from chess import gamerules
from chess.models import Tournament, Game, Move, AccountPage
from chess.forms import AccountPageForm, TournamentForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from copy import deepcopy

class IndexView(View):
    def get(self, request):
        return render(request, 'chess/index.html')

class PlayView(View):
    def get(self, request, game_id):
        try:
            game = Game.objects.get(id=game_id)

            # if spectate_mode is on, the user will have no control over the game
            spectate_mode = 'spectate' in request.path.split('/')

            if timezone.now() < game.time: # dissalow users from entering games which are scheduled in the future
                return redirect(reverse('chess:index'))
            elif game.result is not None: # if the game has been played already, redirect user to its history page
                return redirect(reverse('chess:gamehistory', kwargs={'game_id':game_id}))

            # perspective decides if the board is shown normal or upside down
            perspective = 0
            if not spectate_mode:
                if request.user.is_authenticated and request.user == game.player_white:
                    perspective = 0
                elif request.user.is_authenticated and request.user == game.player_black:
                    perspective = 1
                else:
                    # user does not participate in this game
                    return redirect(reverse('chess:spectate', kwargs={'game_id':game_id}))

            # execute moves on the board in order
            board_state = deepcopy(gamerules.starting_board_state)
            moves = Move.objects.filter(game=game).order_by('move_id')
            for move in moves:
                gamerules.make_move(board_state, move.square_from, move.square_to)

            context_dict = {'perspective': perspective, 
                            'board_state': board_state, 
                            'moves': [move.square_from + move.square_to for move in moves], 
                            'spectate_mode': spectate_mode,
                            'player_white_name': game.player_white.username,
                            'player_black_name': game.player_black.username}
            
            return render(request, 'chess/play.html', context_dict)
        except Game.DoesNotExist:
            return redirect(reverse('chess:index'))

class PlayLobbyView(View):
    def get(self, request):
        games = Game.objects.filter(time__lte=timezone.now()).filter(result__isnull=True)
        if request.user.is_authenticated:
            ongoing_games = games.exclude(player_black=request.user).exclude(player_white=request.user)
            games_white = games.filter(player_white=request.user)
            games_black = games.filter(player_black=request.user)
            playable_games = (games_white | games_black)
        else:
            ongoing_games = games
            playable_games = None

        # playable games are the currently held games which the user participates in. ongoing games are all other currently held games.
        context_dict = {'playable_games': playable_games.order_by('time'), 'ongoing_games': ongoing_games.order_by('time') }

        # gamestatus is present if the user has just finished their game. It informs them if they won, lost or drawn the game
        if 'gamestatus' in request.GET:
            gamestatus = request.GET['gamestatus']
            if gamestatus == 'draw':
                context_dict['message'] = "Your game ended in a draw."
            elif gamestatus == 'win':
                context_dict['message'] = "Congratulations! You have won the game."
            elif gamestatus == 'loss':
                context_dict['message'] = "You have lost the game."
        
        return render(request, 'chess/playlobby.html', context_dict)

class MoveListView(View):
    def get(self, request, game_id):
        try:
            game = Game.objects.get(id=game_id)

            # execute moves on the board in order
            board_state = deepcopy(gamerules.starting_board_state)
            moves = Move.objects.filter(game=game).order_by('move_id')
            for move in moves:
                gamerules.make_move(board_state, move.square_from, move.square_to)

            # board_state['turn'] is false when it's white player's turn, true otherwise
            turn = board_state['turn']==(request.user==game.player_black)
            
            move_str = request.GET['move']
            if move_str and (move_str in gamerules.legal_moves(board_state)): # double checks if the received move is valid
                # create a new move in db
                move = Move()
                move.game = game
                move.square_from = move_str[:2]
                move.square_to = move_str[2:]
                move.save()
                # update the board 
                gamerules.make_move(board_state, move.square_from, move.square_to)
                # now is the turn of the opponent
                turn = False

                # check if the current position is winning/losing/tied
                if gamerules.mate_white(board_state):
                    game.result = 0.0 # black won (0-1)
                    game.save()
                elif gamerules.mate_black(board_state):
                    game.result = 1.0 # white won (1-0)
                    game.save()
                elif gamerules.draw(board_state):
                    game.result = 0.5 # draw (1/2-1/2)
                    game.save()

            # if the game is already decided, redirect to playlobby with a message
            if game.result is not None:
                if game.result == 0.5:
                    gamestatus = 'draw'
                elif ((game.result == 0.0 and request.user == game.player_black) or 
                        (game.result == 1.0 and request.user == game.player_white)):
                    gamestatus = 'win'
                else:
                    gamestatus = 'loss'
                return JsonResponse({'redirect':reverse('chess:playlobby')+'?gamestatus='+gamestatus})
            
            return JsonResponse({'turn':turn, 'legal_moves':gamerules.legal_moves(board_state)})
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
            
class GameHistoryView(View):
    def get(self, request, game_id):
        try:
            game = Game.objects.get(id=game_id)

            if timezone.now() < game.time:
                return redirect(reverse('chess:index'))
            elif game.result is None:
                redirect(reverse('chess:play', kwargs={'game_id':game_id}))

            moves = Move.objects.filter(game=game).order_by('move_id')

            context_dict = { 'moves': [move.square_from + move.square_to for move in moves]}
            return render(request, 'chess/gamehistory.html', context_dict)
        except Game.DoesNotExist:
            return redirect(reverse('chess:index'))

class BoardHistoryView(View):
    def get(self, request, game_id):
        try:
            game = Game.objects.get(id=game_id)
            moves = Move.objects.filter(game=game).order_by('move_id')

            if 'move_index' in request.GET:
                n_moves = int(request.GET['move_index'])
            else:
                n_moves = moves.count()

            board_state = deepcopy(gamerules.starting_board_state)
            for move in moves[:n_moves]:
                gamerules.make_move(board_state, move.square_from, move.square_to)

            context_dict = {'perspective': 0, 
                            'board_state': board_state,
                            'player_white_name': game.player_white.username,
                            'player_black_name': game.player_black.username}
            return HttpResponse(render_to_string('chess/board.html', context_dict))
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

class CalendarUpdateView(View):
    def get(self, request):
        tournaments = Tournament.objects.all()

        event_list = []

        for tournament in tournaments:
            event_list.append({'title':tournament.name, 'start':tournament.date.strftime('%Y-%m-%dT%H:%M:%S')})
        
        return JsonResponse(event_list, safe=False)

@login_required
def create_accountpage(request):
    if request.method == 'POST':
        accountpage = AccountPage.objects.get_or_create(user=request.user)[0]
        accountpage_form = AccountPageForm(request.POST, request.FILES, instance=accountpage)
        
        if accountpage_form.is_valid():
            accountpage_form.save(commit=True)
            return redirect(reverse('chess:accountpage'))
        else:
            print(accountpage_form.errors)
    else:
        accountpage_form = AccountPageForm()
   
    return render(request, 'chess/create_accountpage.html', {'accountpage_form': accountpage_form})

def show_accountpage(request):
    context_dict = {}
    
    try:
        accountpage = AccountPage.objects.get(user=request.user)
        context_dict['accountpage'] = accountpage
    except AccountPage.DoesNotExist:
        context_dict['accountpage'] = None
    
    return render(request, 'chess/accountpage.html', context=context_dict)

@login_required
def add_tournament(request):
    tournament_form = TournamentForm()
    
    if request.method == 'POST':
        tournament_form = TournamentForm(request.POST)
        if tournament_form.is_valid():
            tournament_form.save(commit=True)
            return redirect(reverse('chess:history'))
        else:
            print(form.errors)
    return render(request, 'chess/add_tournament.html', {'tournament_form': tournament_form})