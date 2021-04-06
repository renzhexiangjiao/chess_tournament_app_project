$(function() {
    if($('#chess-board').length) {
        $.get('/chess/moveupdate/', function(data) {
            /*alert(data);*/ 
        });
    }

    var movelist = [];
    var sq_from = null;
    var sq_to = null;

    $.get('/chess/movelist/', { move: sq_from + sq_to },
    function(data) {
        movelist = data.split(' ');
    });

    for(let c = 10; c < 18; c++) {
        for(let r = 1; r < 9; r++) {
            $('#'+c.toString(36)+r).click(function() {
                if (sq_from && movelist.includes(sq_from + c.toString(36) + r)) {
                    sq_to = c.toString(36) + r
                    $.get('/chess/movelist/', { move: sq_from + sq_to },
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