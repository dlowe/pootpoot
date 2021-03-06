function play_pootris () {
function _fixposition(X,Y,total_position) {
    var position = total_position;
    if (position == (2 * (X + Y))) {
        position = 0;
    }
    if (position == -1) {
        position = (2 * (X + Y)) - 1;
    }
    return position;
}

function _xy(x,y) {
    return $("#pootris_" + x + '_' + y);
}

function _edge(X,Y,position,c) {
    var x       = 0;
    var y       = 0;
    var drop_x  = 0;
    var drop_y  = 0;
    var delta_x = 0;
    var delta_y = 0;

    if (position < X) {
        x       = position + 1;
        y       = 0;
        drop_x  = x;
        drop_y  = 1;
        delta_y = 1;
        if (c == 'P') {
            delta_x = 1;
        } else if (c == 'O') {
            delta_x = 0;
        } else {
            delta_x = -1;
        }
    } else if (position < (X+Y)) {
        x       = X + 1;
        y       = position - X + 1;
        drop_x  = X;
        drop_y  = y;
        delta_x = -1;
        if (c == 'P') {
            delta_y = 1;
        } else if (c == 'O') {
            delta_y = 0;
        } else {
            delta_y = -1;
        }
    } else if (position < (X+Y+X)) {
        x       = (X + 1) - (position - X - Y + 1);
        y       = Y + 1;
        drop_x  = x;
        drop_y  = Y;
        delta_y = -1;
        if (c == 'P') {
            delta_x = -1;
        } else if (c == 'O') {
            delta_x = 0;
        } else {
            delta_x = 1;
        }
    } else {
        x       = 0;
        y       = (Y + 1) - (position - X - Y - X + 1);
        drop_x  = 1;
        drop_y  = y;
        delta_x = 1;
        if (c == 'P') {
            delta_y = -1;
        } else if (c == 'O') {
            delta_y = 0;
        } else {
            delta_y = 1;
        }
    }

    return {
        'edgebox': _xy(x, y),
        'dropbox': _xy(drop_x, drop_y),
        'drop_x':  drop_x,
        'drop_y':  drop_y,
        'delta_x': delta_x,
        'delta_y': delta_y
    };
}

function _c(string) {
    return string.charAt(r(0,(string.length-1)));
}

function pootris (target, X, Y, string, timeout) {
    var h = '<div id="instructions">';
    h += 'controls: A, S, D<br/>';
    h += 'goal: spell ' + string;
    h += '</div>';
    h += '<table id="pootris_table" cellpadding=0 cellspacing=0>';
    for (var y = 0; y < (Y + 2); ++y) {
        h += '<tr>';
        for (var x = 0; x < (X + 2); ++x) {
            h += '<td id="pootris_' + x + '_' + y + '"/>';
        }
        h += '</tr>';
    }
    h += '</table>';
    h += '<div id="scoreboard">0</div>';
    target.html(h);

    $("#pootris_table").css({'margin':       '0px auto',
                             'border-width': 2,
                             'border-style': 'solid',
                             'color':        '#FFFFFF'});
    for (var y = 0; y < (Y + 2); ++y) {
        for (var x = 0; x < (X + 2); ++x) {
            _xy(x, y).css({
                'width':            12,
                'min-width':        12,
                'max-width':        12,
                'height':           24,
                'min-height':       24,
                'max-height':       24,
                'overflow':         'hidden',
                'text-align':       'center',
                'font-family':      'Impact,sans-serif',
                'color':            '#FFFFFF',
                'background-color': '#000000'
            });
            _xy(x, y).text(' ');
        }
    }
    // inside border...
    _xy(1, 1).css({'border-style': 'dotted none none dotted', 'border-width': 'thin'});
    _xy(1, Y).css({'border-style': 'none none dotted dotted', 'border-width': 'thin'});
    _xy(X, 1).css({'border-style': 'dotted dotted none none', 'border-width': 'thin'});
    _xy(X, Y).css({'border-style': 'none dotted dotted none', 'border-width': 'thin'});
    for (var x = 2; x < X; ++x) {
        _xy(x, 1).css({'border-style': 'dotted none none none', 'border-width': 'thin'});
        _xy(x, Y).css({'border-style': 'none none dotted none', 'border-width': 'thin'});
    }
    for (var y = 2; y < Y; ++y) {
        _xy(1, y).css({'border-style': 'none none none dotted', 'border-width': 'thin'});
        _xy(X, y).css({'border-style': 'none dotted none none', 'border-width': 'thin'});
    }
    $("#instructions").css({'margin':      '10px auto',
                            'width':       $("#pootris_table").width() + 10,
                            'font-family': 'Impact,sans-serif'});
    $("#scoreboard").css({'margin':           '0px auto',
                          'width':            $("#pootris_table").width() - 20,
                          'height':           24,
                          'font-family':      'Impact,sans-serif',
                          'text-align':       'right',
                          'color':            '#FFFFFF',
                          'background-color': '#000000',
                          'border-width':     2,
                          'border-style':     'solid'});

    var piece = function () {
        var ready    = 1;
        var position = 0;
        var c        = _c(string);
        var edge     = _edge(X,Y,position,c);
        var score    = 0;
        edge.edgebox.text(c);

        return {
            'counterclockwise': function () {
                if (ready) {
                    edge.edgebox.text(' ');
                    position = _fixposition(X,Y,position - 1);
                    edge = _edge(X,Y,position,c);
                    edge.edgebox.text(c);
                }
            },
            'clockwise': function () {
                if (ready) {
                    edge.edgebox.text(' ');
                    position = _fixposition(X,Y,position + 1);
                    edge = _edge(X,Y,position,c);
                    edge.edgebox.text(c);
                }
            },
            'drop': function () {
                if (ready && (edge.dropbox.text() == ' ')) {
                    ready = 0;
                    edge.edgebox.text(' ');

                    // drop piece
                    edge.dropbox.text(c);
                    var dx = edge.delta_x;
                    var dy = edge.delta_y;
                    var x  = edge.drop_x;
                    var y  = edge.drop_y;

                    var animate = function () {
                        if ((x + dx) == (X + 1)) {
                                // bounce off the right wall
                                if (dy == 0) {
                                    dx = 0;
                                    dy = 1;
                                }
                                dx *= -1;
                        } else if ((x + dx) == 0) {
                                // bounce off the left wall
                                if (dy == 0) {
                                    dx = 0;
                                    dy = 1;
                                }
                                dx *= -1;
                        }

                        if ((y + dy) == 0) {
                                // bounce off the ceiling
                                dy *= -1;
                        }

                        if ((_xy(x + dx, y + dy).text() == ' ') && ((y + dy) < (Y + 1))) {
                            // move the piece
                            _xy(x, y).text(' ');
                            x += dx;
                            y += dy;
                            _xy(x, y).text(c);

                            // next!
                            timeout.set(animate);
                        } else {
                            // the piece stopped
                            var clearpoots = function () {
                                var subscore = 1;

                                // remove debris
                                for (var clear_x = 1; clear_x <= X; ++clear_x) {
                                    for (var clear_y = Y; clear_y >= 1; --clear_y) {
                                        while (_xy(clear_x, clear_y).text() == '*') {
                                            for (var drop_y = clear_y; drop_y >= 2; --drop_y) {
                                                _xy(clear_x, drop_y).text(_xy(clear_x, drop_y - 1).text());
                                            }
                                            _xy(clear_x, 1).text(' ');
                                        }
                                    }
                                }
                                
                                // check for new POOT
                                var poot_spots = [];
                                for (var start_x = 1; start_x <= X; ++start_x) {
                                    for (var start_y = 1; start_y <= Y; ++start_y) {
                                        for (var dir_x = -1; dir_x < 2; ++dir_x) {
                                            for (var dir_y = -1; dir_y < 2; ++dir_y) {
                                                var found_poot = 1;
                                                for (var i = 0; i < string.length; ++i) {
                                                    if (string.charAt(i) != _xy(start_x+(i*dir_x), start_y+(i*dir_y)).text()) {
                                                        found_poot = 0;
                                                    }
                                                }
                                                if (found_poot) {
                                                    for (var i = 0; i < string.length; ++i) {
                                                        poot_spots.push([start_x+(i*dir_x), start_y+(i*dir_y)]);
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                                if (poot_spots.length) {
                                    for (var i = 0; i < poot_spots.length; ++i) {
                                        subscore *= 2;
                                        _xy(poot_spots[i][0], poot_spots[i][1]).text('*');
                                    }
                                    score = score + subscore;
                                    $("#scoreboard").text(score);
                                    timeout.set(clearpoots);
                                } else {
                                    score = score + subscore;
                                    $("#scoreboard").text(score);

                                    // check for game over
                                    var game_over = 1;
                                    for (var cx = 0; cx < X; ++cx) {
                                        if (_xy(cx + 1, 1).text() == ' ') {
                                            game_over = 0;
                                        }
                                        if (_xy(cx + 1, Y).text() == ' ') {
                                            game_over = 0;
                                        }
                                    }
                                    for (var cy = 0; cy < Y; ++cy) {
                                        if (_xy(1, cy + 1).text() == ' ') {
                                            game_over = 0;
                                        }
                                        if (_xy(X, cy + 1).text() == ' ') {
                                            game_over = 0;
                                        }
                                    }
                                    if (! game_over) {
                                        // next piece!
                                        position = 0;
                                        c        = _c(string);
                                        edge     = _edge(X,Y,position,c);
                                        edge.edgebox.text(c);
                                        ready = 1;
                                    } else {
                                        var go  = "GAME OVER";
                                        var gox = Math.floor((X - go.length) / 2);
                                        var goy = Math.floor(Y / 2);
                                        for (var n = 0; n < go.length; ++n) {
                                            var s = _xy(gox + n + 1, goy);
                                            s.text(go.charAt(n));
                                            s.css({'color': '#FF0000'});
                                        }
                                    }
                                }
                            };
                            clearpoots();
                        }
                    };
                    timeout.set(animate);
                }
            }
        }
    }();

    shortcut.add('A',  piece.counterclockwise, {'type': 'keypress'});
    shortcut.add('S', piece.clockwise, {'type': 'keypress'});
    shortcut.add('D', piece.drop);
}

var timeout_id = null;
var timeout = {
    'set': function (f) {
        timeout_id = setTimeout(f, 40);
    },
    'clear': function () {
        clearTimeout(timeout_id);
    }
};

return {
    'start': function (target) { pootris(target, 15, 12, "POOT", timeout) },
    'stop':  function () {
        timeout.clear();
        shortcut.remove('A');
        shortcut.remove('S');
        shortcut.remove('D');
    }
};
}
