function r (a,b) {
    return (Math.floor(Math.random()*(b-a+1)) + a);
}

function random_color () {
   var color = "#";
   for (var i = 1; i <= 6; ++i) {
       color += "0123456789ABCDEF".charAt(r(0, 15));
   }
   return color;
}

function colorize (target) {
   target.css("background-color", random_color());
   target.css("color", random_color());
}

function poot (target) {
    $.ajaxSetup({ cache: false });
    $.getJSON("/poot", function (json) {
        if (json.type == "javascript") {
            $.ajaxSetup({ cache: true });
            $.getScript(json.location, function () {
                target.empty();
                colorize(target);
                pootpoot(target);
            });
        } else if (json.type == "text") {
            $.ajaxSetup({ cache: true });
            $.get(json.location, function (data) {
                target.empty();
                colorize(target);
                target.append("<pre>" + data + "</pre>");
            }, "text");
        } else if (json.type == "image") {
            target.empty();
            colorize(target);
            target.append("<center><img src=\"" + json.location + "\"/></center>");
        }
    });
}
