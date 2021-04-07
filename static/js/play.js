$(function() {
    var pathname = window.location.pathname.split('/');
    var game_id = pathname[pathname.length - 2];
        
    var last_move = '';
    var movelist = [];
    var sq_from = null;
    var sq_to = null;

    function updateBoard() {
        $.get('/chess/moveupdate/'+game_id+'/', function(data) {
            if (data != last_move) {
                last_move = data;
                $('#'+last_move.substring(0,2)).remove('.selector');
                $('#'+last_move.substring(2)).html($('#'+last_move.substring(0,2)).html());
                $('#'+last_move.substring(0,2)).html('');
                $('#move-list').append(`<li>${data}</li>`);
                $.get('/chess/movelist/'+game_id+'/', { move: sq_from + sq_to },
                function(data) {
                    movelist = data.split(' ');
                });
            }
        });
    }
    updateBoard();
    setInterval(updateBoard, 5000);
    
    for(let c = 10; c < 18; c++) { // columns a to h
        for(let r = 1; r < 9; r++) { // rows 1 to 8
            $('#'+c.toString(36)+r).click(function() {
                if (sq_from && movelist.includes(sq_from + c.toString(36) + r)) {
                    sq_to = c.toString(36) + r
                    last_move = sq_from + sq_to
                    $('#'+sq_to).html($('#'+sq_from).html());
                    $('#'+sq_from).html('');
                    $.get('/chess/movelist/'+game_id+'/', { move: sq_from + sq_to },
                    function(data) {
                        movelist = data.split(' ');
                    });
                    $('img').remove('.selector');
                    sq_to = null;
                    sq_from = null;
                } else {
                    $('img').remove('.selector');
                    sq_to = null;
                    sq_from = c.toString(36) + r;
                    for(let i = 0; i < movelist.length; i++) {
                        if (movelist[i].startsWith(sq_from)) {
                            $('#'+movelist[i].substring(2)).append('<img class="selector" src="/static/images/selector.png" alt="O">');
                        }
                    }
                }
            });
        }
    }
});