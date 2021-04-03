$(function() {
    if($('#chess-board').length) {
        $.get('/chess/moveupdate/', function(data) {
            /*alert(data);*/
        });
        
        var white = true;
        var chessBoard = [  {'a':'white/rook.png','b':'white/knight.png','c':'white/bishop.png','d':'white/queen.png','e':'white/king.png','f':'white/bishop.png','g':'white/knight.png','h':'white/rook.png'},
                            {'a':'white/pawn.png','b':'white/pawn.png','c':'white/pawn.png','d':'white/pawn.png','e':'white/pawn.png','f':'white/pawn.png','g':'white/pawn.png','h':'white/pawn.png'},
                            {'a':'','b':'','c':'','d':'','e':'','f':'','g':'','h':''},
                            {'a':'','b':'','c':'','d':'','e':'','f':'','g':'','h':''},
                            {'a':'','b':'','c':'','d':'','e':'','f':'','g':'','h':''},
                            {'a':'','b':'','c':'','d':'','e':'','f':'','g':'','h':''},
                            {'a':'black/pawn.png','b':'black/pawn.png','c':'black/pawn.png','d':'black/pawn.png','e':'black/pawn.png','f':'black/pawn.png','g':'black/pawn.png','h':'black/pawn.png'},
                            {'a':'black/rook.png','b':'black/knight.png','c':'black/bishop.png','d':'black/queen.png','e':'black/king.png','f':'black/bishop.png','g':'black/knight.png','h':'black/rook.png'}];

        var s = '';
        for(var i = 0; i < 8; i++) {
            for(var j = 10; j <= 17; j++) {
                s += `<div id="${(white?j:27-j).toString(36)}${white?8-i:i+1}" style="grid-area: ${i+2} / ${j-8} / ${i+3} / ${j-7};">` + (chessBoard[white?7-i:i][(white?j:27-j).toString(36)]?`<img src="/static/images/pieces/${chessBoard[white?7-i:i][(white?j:27-j).toString(36)]}" alt="piece">`:'') + '</div>';
            }
        }
        $('#chess-board').append(s);
        if(!white) {
            $('#chess-board').css('background-image', "url('/static/images/chessboard-rotated.png')");
        }
    }
    $('#submit-move').click(function () {
        $.get('/chess/movelist/', { move: $('#move-dropdown').val() },
        function(data) {
            if ($('#move-dropdown').val()) {
                $('#move-list').append('<li>' + $('#move-dropdown').val() + '</li>')
            }
            $('#move-dropdown').html(data);
        });
    });
});