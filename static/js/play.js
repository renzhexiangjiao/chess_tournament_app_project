$(function() {
    var pathname = window.location.pathname.split('/');
    var game_id = pathname[pathname.length - 2];
        
    var second_last_move = $('#move-list li').last().prev().html();
    var last_move = $('#move-list li').last().html();

    var legal_moves = [];
    var sq_from = null;
    var sq_to = null;

    var turn = false;

    function updateLegalMoves(new_move) {
        // ask server for legal moves
        $.get('/chess/movelist/'+game_id+'/', { move: new_move },
        function(data) {
            if(data.redirect) {
                $(location).attr('href', data.redirect);
            } else {
                turn = data.turn;
                legal_moves = data.legal_moves;
            }
        });
    }

    function updateBoard() {
        $.get('/chess/moveupdate/'+game_id+'/', function(data) {
            // if the opponent made a move in last 0.5s
            if (data != last_move && data != second_last_move) {

                // update second last and last moves
                second_last_move = last_move;
                last_move = data;

                // move the piece on the board
                $('#'+last_move.substring(0,2)).remove('.selector');
                $('#'+last_move.substring(2)).html($('#'+last_move.substring(0,2)).html());
                $('#'+last_move.substring(0,2)).html('');

                // update the list
                $('#move-list').append(`<li>${data}</li>`);

                // ask server for legal moves
                updateLegalMoves('');
            }
        });
    }

    // check for board updates every 0.5s
    updateBoard();
    updateLegalMoves('');
    setInterval(updateBoard, 500);
    
    // set up click listeners
    for(let c = 10; c < 18; c++) { // columns a to h
        for(let r = 1; r < 9; r++) { // rows 1 to 8
            let clicked_square = c.toString(36) + r;
            $('#'+clicked_square).click(function() {
                if(turn) {
                    // case 1: player clicked a green circle
                    if (sq_from && legal_moves.includes(sq_from + clicked_square)) {
                        sq_to = clicked_square;

                        // update second last and last moves
                        second_last_move = last_move
                        last_move = sq_from + sq_to

                        // move the piece on the board
                        $('#'+sq_to).html($('#'+sq_from).html());
                        $('#'+sq_from).html('');

                        // update the list
                        $('#move-list').append(`<li>${sq_from+sq_to}</li>`);
                        
                        // prevent making any other moves before a new list of moves is received from the server
                        turn = false;

                        // ask server for a new list of legal moves
                        updateLegalMoves(sq_from + sq_to);

                        // remove all green circles
                        $('img').remove('.selector');
                        sq_to = null;
                        sq_from = null;

                    // case 2: player selected a piece to move
                    } else {
                        // remove all existing selectors (green circles)
                        $('img').remove('.selector');

                        sq_to = null;
                        sq_from = clicked_square;

                        // draw selectors (green circles) on tiles which the selected piece can move to
                        for(let i = 0; i < legal_moves.length; i++) {
                            if (legal_moves[i].startsWith(sq_from)) {
                                $('#'+legal_moves[i].substring(2)).append('<img class="selector" src="/static/images/selector.png" alt="O">');
                            }
                        }
                    }
                }
            });
        }
    }
});