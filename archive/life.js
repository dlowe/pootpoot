function life () {
var current = [
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,1,1,1,1,0,0,0,1,1,1,0,0,0,1,1,1,0,0,1,1,1,1,1,0,0],
[0,0,1,0,0,0,1,0,1,0,0,0,1,0,1,0,0,0,1,0,0,0,1,0,0,0,0],
[0,0,1,0,0,0,1,0,1,0,0,0,1,0,1,0,0,0,1,0,0,0,1,0,0,0,0],
[0,0,1,1,1,1,0,0,1,0,0,0,1,0,1,0,0,0,1,0,0,0,1,0,0,0,0],
[0,0,1,0,0,0,0,0,1,0,0,0,1,0,1,0,0,0,1,0,0,0,1,0,0,0,0],
[0,0,1,0,0,0,0,0,0,1,1,1,0,0,0,1,1,1,0,0,0,0,1,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
];

function _xy(x,y) {
    return $("#life_" + x + '_' + y);
}

function _live_neighbors(X,Y,x,y) {
    var live = 0;
    for (var dx = -1; dx < 2; ++dx) {
        if (((x + dx) >= 0) && ((x + dx) < X)) {
            for (var dy = -1; dy < 2; ++dy) {
                if (((y + dy) >= 0) && ((y + dy) < Y)) {
                    if (! ((dx == 0) && (dy == 0))) {
                        live += _is_alive(x+dx, y+dy);
                    }
                }
            }
        }
    }
    return live;
}

function _is_alive(x,y) {
    return _xy(x, y).hasClass('alive');
}

function _life (target, X, Y, start, timeout) {

    var h = '<table id="life_table" cellpadding=0 cellspacing=0';
    for (var y = 0; y < Y; ++y) {
        h += '<tr>';
        for (var x = 0; x < X; ++x) {
            h += '<td id="life_' + x + '_' + y + '"/>';
        }
        h += '</tr>';
    }
    h += '</table>';
    // h += '<textarea id="debug" rows=100 cols=80></textarea>';
    target.html(h);

    $("#life_table").css({'margin': '10px auto',
                          'border-width': 1,
                          'border-style': 'solid',
                          'color':        '#000000'});

    for (var y = 0; y < Y; ++y) {
        for (var x = 0; x < X; ++x) {
            var color;
            if (start[y][x] == 1) {
                _xy(x, y).addClass('alive');
                color = '#000000';
            } else {
                _xy(x, y).removeClass('alive');
                color = '#FFFFFF';
            }

            _xy(x, y).css({
                'width':            10,
                'min-width':        10,
                'max-width':        10,
                'height':           10,
                'min-height':       10,
                'max-height':       10,
                'overflow':         'hidden',
                'color':            '#000000',
                'background-color': color,
                'border-width':     'thin',
                'border-style':     'dotted'
            });
        }
    }

    var next = new Array(Y);
    for (var y = 0; y < Y; ++y) {
        next[y] = new Array(X);
    }

    var animate = function () {
        // compute the next step
        for (var x = 0; x < X; ++x) {
            for (var y = 0; y < Y; ++y) {
                var live_neighbors = _live_neighbors(X, Y, x, y);
                //$("#debug").append("(" + x + "," + y + ") bit: " + _is_alive(x, y) + "\n");
                //$("#debug").append("(" + x + "," + y + ") has " + live_neighbors + "\n");
                if (_is_alive(x, y)) {
                    if (live_neighbors < 2) {
                        next[y][x] = 0;
                    } else if (live_neighbors > 3) {
                        next[y][x] = 0;
                    } else {
                        next[y][x] = 1;
                    }
                } else {
                    if (live_neighbors == 3) {
                        next[y][x] = 1;
                    } else {
                        next[y][x] = 0;
                    }
                }
            }
        }

        // draw it
        for (var x = 0; x < X; ++x) {
            for (var y = 0; y < Y; ++y) {
                var color;
                if (next[y][x] == 1) {
                    color = '#000000';
                    _xy(x, y).addClass('alive');
                } else {
                    color = '#FFFFFF';
                    _xy(x, y).removeClass('alive');
                }

                _xy(x, y).css({'background-color': color});
            }
        }

        timeout.set(animate);
    }
    timeout.set(animate);
}

var timeout_id = null;
var timeout = {
    'set': function (f) {
        timeout_id = setTimeout(f, 200);
    },
    'clear': function () {
        clearTimeout(timeout_id);
    }
};

return {
    'start': function (target) {
        _life(target, current[0].length, current.length, current, timeout);
    },
    'stop': function () {
        timeout.clear();
    }
};
}
