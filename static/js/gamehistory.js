$(function(){
    var pathname = window.location.pathname.split('/');
    var game_id = pathname[pathname.length - 2];

    var n_moves = $('#move-list li').length;
    var current_move_index = n_moves - 1;
    
    function updateBoard() {
        $.get('/chess/board-history/'+game_id+'/', {'move_index': current_move_index},
        function(data) {
            $('#chess-board-container').html(data);
        });
        $('#move-list li').css('background-color', 'white')
        $('#move-list li').eq(current_move_index).css('background-color', '#22EE22')
    }

    updateBoard();

    $('#prev-move').click(function() {
        if (current_move_index > 0) {
            current_move_index--;
            updateBoard();
        }
    });
    $('#next-move').click(function() {
        if (current_move_index < n_moves - 1) {
            current_move_index++;
            updateBoard();
        }
    });
});