$(function() {
    var pathname = window.location.pathname.split('/');
    var game_id = pathname[pathname.length - 2];
        
    var second_last_move = $('#move-list li').last().prev().html();
    var last_move = $('#move-list li').last().html();

    function updateBoard() {
        $.get('/chess/moveupdate/'+game_id+'/', function(data) {
            // if someone made a move in last 0.5s
            if (data != last_move && data != second_last_move) {

                // update second last and last moves
                second_last_move = last_move;
                last_move = data;

                // move the piece on the board
                $('#'+last_move.substring(2)).html($('#'+last_move.substring(0,2)).html());
                $('#'+last_move.substring(0,2)).html('');

                // update the list
                $('#move-list').append(`<li>${data}</li>`);
            }
        });
    }

    // check for board updates every 0.5s
    updateBoard();
    setInterval(updateBoard, 500);
});