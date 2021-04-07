import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'chess_tournament_app_project.settings')

import django
django.setup()
from chess.models import Tournament, Game

def populate():
    
    tournament1_games = [
        {'time': '14:00',
         'player_white':'Jack',
         'player_black':'John'},
        {'time': '14:00',
          'player_white':'Jerry',
          'player_black':'Kristen'},
        {'time': '15:00',
         'player_white':'Jack',
         'player_black':'Kristen'},
         {'time': '15:00',
         'player_white':'John',
         'player_black':'Jerry'}]
         
    tournament2_games = [
        {'time': '14:00',
         'player_white':'Tom',
         'player_black':'John'},
        {'time': '14:45',
          'player_white':'Jessica',
          'player_black':'Kristen'},
        {'time': '15:30',
         'player_white':'Jack',
         'player_black':'Chris'},
         {'time': '16:15',
         'player_white':'Harry',
         'player_black':'Jerry'}]
    
    tournaments = {'Tournament1': {'date': '08/3/2021', 'games': tournament1_games},
            'Tournament2': {'date': '20/3/2021', 'games': tournament2_games},
            'Tournament3': {'date': '10/04/2021', 'games': []}}
            
    
    for tournament, tournament_data in tournaments.items():
        t = add_tournament(tournament, tournament_data['date'])
        for g in tournament_data['games']:
            add_game(t, g['time'], g['player_white'], g['player_black'])
        
    
    for t in Tournament.objects.all():
        for g in Game.objects.filter(tournament=t):
            print(f'- {t}: {g}')

def add_tournament(name, date):
    t = Tournament.objects.get_or_create(name=name)[0]
    t.date = date
    t.save()
    return t

def add_game(tournament, time, player_white, player_black):
    g = Game.objects.get_or_create(tournament=tournament, player_white = player_white, player_black = player_black)[0]
    g.time = time
    g.save()
    return g

# Start execution here!
if __name__ == '__main__':
    print('Starting Chess population script...')
    populate()