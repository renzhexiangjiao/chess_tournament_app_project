$(function() {
    if($('#chessboard')) {
        $.get('/chess/moveupdate/', function(data) {
            alert(data);
        });
        $('#submit-move').click(function () {
            $.get('/chess/movelist/', { move: $('#move-dropdown').val() },
            function(data) {
                if ($('#move-dropdown').val()) {
                    $('#move-list').append('<li>' + $('#move-dropdown').val() + '</li>')
                }
                $('#move-dropdown').html(data);
            });
        });
    }
});