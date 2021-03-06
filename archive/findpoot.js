function find_poot_classic () {
function _css_box(target) {
    target.css({ 'width':        100,
                 'min-width':    100,
                 'max-width':    100,
                 'overflow':     'hidden',
                 'text-align':   'center',
                 'border-width': 'medium',
                 'border-style': 'solid',
                 'border-color': 'blue',
                 'font-size':    '2.2em',
                 'font-family':  'Impact,sans-serif',
                 'font-weight':  'bold',
                 'background-color': '#000000' });
}

function _find_poot(target, rows, columns, level, message, interval) {
    var remaining_time = 10;

    var splash_html = '<div id="find_poot_splash" style="display:none"><h1>' + message + '</h1><h2>Find the yellow Poot in less than 10 seconds!</h2><h2>To start the game press the yellow Poot</h2><table id="find_poot_splash_table" cellpadding=1 cellspacing=1><tr><td id="green_poot"/><td id="yellow_boot"/><td id="yellow_poot"/></tr></table></div>';
    var table_html = '<div id="find_poot" style="display:none"><table id="find_poot_table" height="304" cellpadding=1 cellspacing=1>';
    for (var row = 0; row < rows; row++) {
        table_html += '<tr>';
        for (var col = 0; col < columns; col++) {
            table_html += '<td id="find_poot_' + row + '_' + col + '"/>';
        }
        table_html += '</tr>';
    }
    table_html += '</table>';
    table_html += '<table id="timer" width=600 height=15 cellpadding=1 cellspacing=1 border=2><tr>';
    for (var t = remaining_time; t > 0; t--) {
        table_html += '<td id="timerbox_' + t + '"/>';
    }
    table_html += '</tr></table>';
    table_html += '</div>';
    target.html(splash_html + table_html);

    poot_row = r(0, rows-1);
    poot_col = r(0, columns-1);

    // set up the splash...
    $("#find_poot_splash").css({'margin':     '0px auto',
                                'width':      '500px'});
    $("#find_poot_splash_table").css({'background-color': '#000000',
                                      'margin':           '0px auto'});
    _css_box($("#green_poot"));
    $("#green_poot").css('color', 'green');
    $("#green_poot").text('Poot');
    _css_box($("#yellow_boot"));
    $("#yellow_boot").css('color', 'yellow');
    $("#yellow_boot").text('Boot');
    _css_box($("#yellow_poot"));
    $("#yellow_poot").css('color', 'yellow');
    $("#yellow_poot").text('Poot');
    $("#yellow_poot").click(function () {
        // hide splash and show game
        $("#find_poot_splash").hide();
        // start the timer
        $("#timer").css('background-color', 'black');
        $("#timer").css('margin', 'auto');
        for (var t = remaining_time; t > 0; t--) {
            var selector = "#timerbox_" + t;
            var box = $(selector);

            box.css({'background-color': 'black'});
        }
        $("#find_poot").show();
        interval.set(function () {
            --remaining_time;
            $("#timerbox_" + (remaining_time + 1)).css('background-color', 'yellow');
            if (remaining_time == 0) {
                interval.clear();
                $("#find_poot").hide();
                _find_poot(target, rows, columns, level, "Time's up!! Try again!", interval);
            }
        }, 1000);
    });

    // set up the game
    $("#find_poot_table").css({'background-color': '#000000',
                               'margin':           '0px auto'});
    for (var row = 0; row < rows; row++) {
        for (var col = 0; col < columns; col++) {
            var selector = "#find_poot_" + row + "_" + col;
            var t = $(selector);

            t.mouseover(function(r_row,r_col,r_t) {
                return function () {
                    if ((r_row == poot_row) && (r_col == poot_col)) {
                        r_t.css('color', 'yellow');
                        r_t.text('Poot');
                    } else {
                        r_t.css('color', 'yellow');
                        r_t.text('Boot');
                    }
                }
            }(row, col, t));

            t.mouseout(function(r_t) {
                return function () {
                    r_t.css('color', 'green');
                    r_t.text('Poot');
                }
            }(t));

            t.click(function(r_row, r_col) {
                return function () {
                    if ((r_row == poot_row) && (r_col == poot_col)) {
                        interval.clear();
                        $("#find_poot").hide();
                        _find_poot(target, rows, columns, level + 1, "Nice! Try Level " + (level + 1), interval);
                    } else {
                        interval.clear();
                        $("#find_poot").hide();
                        _find_poot(target, rows, columns, level, "That was Boot!! Try again!", interval);
                    }
                }
            }(row, col));

            _css_box(t);
            t.css('color', 'green');
            t.text('Poot');
        }
    }
    $("#find_poot_splash").show();
}

var interval_id = null;
var interval = {
    'set': function (f, t) {
        interval_id = setInterval(f, t);
    },
    'clear': function () {
        clearInterval(interval_id);
    }
};

return {
    'start': function (target) { _find_poot(target, 4, 5, 1, 'Level 1', interval) },
    'stop':  function () { interval.clear() }
};
}
