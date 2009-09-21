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

function poot_title (target, interpretation) {
    target.html(interpretation.title);
}

function poot (target, key_or_null) {
    arguments = { };
    if (key_or_null) {
        arguments.key = key_or_null;
    }
    $.ajaxSetup({ cache: false });
    $.getJSON("/poot", arguments, function (interpretation) {
        if (interpretation.type == "javascript") {
            $.ajaxSetup({ cache: true });
            $.getScript(interpretation.location, function () {
                colorize(target);
                poot_title(target.find("#title"), interpretation);
                target.find("#content").empty();
                pootpoot(target.find("#content"));
            });
        } else if (interpretation.type == "text") {
            $.ajaxSetup({ cache: true });
            $.get(interpretation.location, function (data) {
                colorize(target);
                poot_title(target.find("#title"), interpretation);
                contents = "<pre>" + data + "</pre>";
                target.find("#content").html(contents);
            }, "text");
        } else if (interpretation.type == "image") {
            colorize(target);
            poot_title(target.find("#title"), interpretation);
            contents = "<center><img alt=\"" + interpretation.title + "\" src=\"" + interpretation.location + "\"/></center>";
            target.find("#content").html(contents);
        }
    });
}
