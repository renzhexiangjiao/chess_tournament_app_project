$(function() {
    if($('#chess-board').length) {
        $.get('/chess/moveupdate/', function(data) {
            /*alert(data);*/ 
        });
    }
    $('#submit-move').click(function () {
        $.get('/chess/movelist/', { move: $('#move-dropdown').val() },
        function(data) {
            let move = $('#move-dropdown').val();
            if (move) {
                $('#move-list').append('<li>' + move + '</li>');
                $('#'+move.substring(2)).html($('#'+move.substring(0,2)).html());
                $('#'+move.substring(0,2)).html("");
            }
            $('#move-dropdown').html(data);
        });
    });
});