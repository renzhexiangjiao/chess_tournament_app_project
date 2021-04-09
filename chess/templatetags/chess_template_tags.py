from django import template
from django.contrib.staticfiles.storage import staticfiles_storage
from django.shortcuts import render
from .. import gamerules

register = template.Library()

@register.inclusion_tag('chess/chessboard.html')
def get_board(perspective, board_state, player_white_name, player_black_name):
    s = ''
    for index, square in enumerate(board_state['board']):
        column = chr(ord('a') + index%8)
        row = 1 + index//8

        if perspective:
            s += f'<div id="{column}{row}" style="grid-area: {2+index//8} / {9-index%8} / span 1 / span 1;">'
        else:
            s += f'<div id="{column}{row}" style="grid-area: {9-index//8} / {2+index%8} / span 1 / span 1;">'


        if square != 0:
            s += f'<img src="{staticfiles_storage.url("images/pieces/" + gamerules.PieceTypes.sprites.value[square])}" alt="{gamerules.PieceTypes(square).name}">'
        s += '</div>'

    s += f'<p style="top: 0;">{player_white_name if perspective else player_black_name}</p>'
    s += f'<p style="bottom: 0;">{player_black_name if perspective else player_white_name}</p>'
            
    return {'init_state': s, 'perspective': perspective}