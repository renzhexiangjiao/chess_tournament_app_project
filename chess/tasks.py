from background_task import background
import chess.models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from random import shuffle, choice
from collections import defaultdict

@background(schedule=60)
def schedule_games(tournament_id):
    try:
        tournament = chess.models.Tournament.objects.get(id=tournament_id)
        participants = list(tournament.participants.values_list('id', flat=True))
        shuffle(participants)
        n = len(participants)

        if n <= 1:
            print("Tournament " + tournament.name + " is cancelled due to lack of participants.")
        elif n == 2: # only one game is played in a 2-participant tournament
            game = chess.models.Game()
            game.tournament = tournament
            game.time = timezone.now()
            game.player_white = User.objects.get(id=participants[0])
            game.player_black = User.objects.get(id=participants[1])
            game.save()
            decide_winner(tournament_id, defaultdict(float), schedule=timedelta(minutes=20, seconds=15))
        else:
            if n % 2 == 1:
                participants.insert(n//2, None)
                n += 1

            pairings = []
            pivot = participants[0]
            rest = participants[1:]
            n_rounds = min(n-1, 6) # max 6 rounds in a tournament

            for i in range(n_rounds): 
                pairings.append(list(zip([pivot]+rest[:n//2-1], rest[:n//2-2:-1])))
                rest.insert(0, rest.pop())

            byes = defaultdict(float)
            swapped = lambda x:(x[1],x[0])

            for i, _round in enumerate(pairings):
                for j, pair in enumerate(_round):
                    if choice([0,1]):
                        _round[j] = swapped(pair) # players have 50% chance to swap colors
                    if None in pair:
                        byes[pair[0] or pair[1]] += 1.0 # player who hasn't got an opponent in this round is granted a point for free
                    else:
                        game = chess.models.Game()
                        game.tournament = tournament
                        game.time = timezone.now() + timedelta(minutes=20*i)
                        game.player_white = User.objects.get(id=_round[j][0])
                        game.player_black = User.objects.get(id=_round[j][1])
                        game.save()
                        # after 1 minute check if both players made a move, and then after 20 min decide the winner of the game
                        game_idle(game.id, schedule=game.time+timedelta(minutes=1))
                        game_timeout(game.id, schedule=game.time+timedelta(minutes=20))
            
            decide_winner(tournament_id, byes, schedule=timedelta(minutes=20*n_rounds, seconds=15))
    except chess.models.Tournament.DoesNotExist:
        pass

@background(schedule=60)
def decide_winner(tournament_id, results):
    tournament = chess.models.Tournament.objects.get(id=tournament_id)
    games = chess.models.Game.objects.filter(tournament=tournament)

    # if any of the games isn't finished, raise an error
    if any([game.result is None for game in games]):
        raise AssertionError("Games still not finished")

    for game in games:
        if game.result == 1.0: # white won
            results[game.player_white.id] += 1
        elif game.result == 0.0: # black won
            results[game.player_black.id] += 1
        elif game.result == 0.5: # draw
            results[game.player_white.id] += 0.5
            results[game.player_black.id] += 0.5
        
    winner_id = max(results, key=results.get)
    winner = User.objects.get(id=winner_id)
    tournament.winner = winner
    tournament.save()

@background(schedule=60)
def game_idle(game_id):
    game = chess.models.Game.objects.get(id=game_id)
    if game.result is None:
        n_moves = chess.models.Move.objects.filter(game=game).count()

        if n_moves == 0:
            game.result = 0.0 # black wins since white didn't make a move
            game.save()
        elif n_moves == 1:
            game.result = 1.0 # white wins since black didn't respond with a move
            game.save()


@background(schedule=60)
def game_timeout(game_id):
    game = chess.models.Game.object.get(id=game_id)
    if game.result is None:
        n_moves = chess.models.Move.objects.filter(game=game).count()

        if n_moves % 2 == 0:
            game.result = 0.0 # black wins
            game.save()
        else:
            game.result = 1.0 # white wins
            game.save()