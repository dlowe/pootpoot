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

function shuffle (v) {
    for(var j, x, i = v.length; i; j = parseInt(Math.random() * i), x = v[--i], v[i] = v[j], v[j] = x);
    return v;
}

function poot_title (target, interpretation) {
    target.html("<a href=\"" + interpretation.decorated_location + "\">" + interpretation.title + "</a> by " + interpretation.author);
}

function list (target, key_or_null) {
    arguments = { };
    if (key_or_null) {
        arguments.key = key_or_null;
    }
    $.ajaxSetup({ cache: false });
    $.ajaxSetup({ error: function () {
    }});
    $.getJSON("/list", arguments, function (interpretation_list) {
        colorize(target);
        var contents = "";
        var shuffled_list = shuffle(interpretation_list)
        for (var i in shuffled_list) {
            contents += "<div class=\"listed_interpretation\"><a href=\"" + shuffled_list[i].decorated_location + "\">" + shuffled_list[i].title + "</a> by " + shuffled_list[i].author + "</div>"
        }
        target.html(contents);
    });
}

function poot (target, key_or_null) {
    arguments = { };
    if (key_or_null) {
        arguments.key = key_or_null;
    }
    $.ajaxSetup({ cache: false });
    $.ajaxSetup({ error: function () {
        colorize(target);
        target.find("#content").empty();
        target.find("#title").empty();
        target.find("#content").html("<center><div id=\"#wtf\" style=\"font-size:4em\">?</div></center>");
    }});
    $.getJSON("/poot", arguments, function (interpretation) {
        if (interpretation.type == "javascript") {
            $.ajaxSetup({ cache: false });
            $.getScript(interpretation.content_location, function () {
                colorize(target);
                poot_title(target.find("#title"), interpretation);
                target.find("#content").empty();
                pootpoot(target.find("#content"));
            });
        } else if (interpretation.type == "text") {
            $.ajaxSetup({ cache: true });
            $.get(interpretation.content_location, function (data) {
                colorize(target);
                poot_title(target.find("#title"), interpretation);
                var contents = "<pre>" + data + "</pre>";
                target.find("#content").html(contents);
            }, "text");
        } else if (interpretation.type == "html") {
            $.ajaxSetup({ cache: true });
            $.get(interpretation.content_location, function (data) {
                colorize(target);
                poot_title(target.find("#title"), interpretation);
                target.find("#content").html(data);
            }, "html");
        } else if (interpretation.type == "image") {
            colorize(target);
            poot_title(target.find("#title"), interpretation);
            var contents = "<center><img alt=\"" + interpretation.title + "\" src=\"" + interpretation.content_location + "\"/></center>";
            target.find("#content").html(contents);
        }
    });
}
