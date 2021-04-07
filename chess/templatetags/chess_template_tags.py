from django import template
from django.contrib.staticfiles.storage import staticfiles_storage
from django.shortcuts import render
from .. import gamerules

register = template.Library()

@register.inclusion_tag('chess/chessboard.html')
def get_board(perspective, board_state):
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
            
    return {'init_state': s, 'perspective': perspective}