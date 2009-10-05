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

function interpretation_arguments (filters) {
    var final_filters = {};
    for (var key in filters) {
        if (filters[key] != null) {
            final_filters[key] = filters[key]
        }
    }
    return final_filters;
}

function list (target, filters) {
    $.ajaxSetup({ cache: false });
    $.ajaxSetup({ error: function () {
    }});
    $.getJSON("/list", interpretation_arguments(filters), function (interpretation_list) {
        colorize(target);
        var contents = "";
        var shuffled_list = shuffle(interpretation_list)
        for (var i in shuffled_list) {
            contents += "<div class=\"listed_interpretation\"><a href=\"" + shuffled_list[i].decorated_location + "\">" + shuffled_list[i].title + "</a> by " + shuffled_list[i].author + "</div>"
        }
        target.html(contents);
    });
}

function poot (target, filters) {
    var content = target.find("#content");

    $.ajaxSetup({ cache: false });
    $.ajaxSetup({ error: function () {
        colorize(target);
        target.find("#title").empty();
        content.html("<center><div id=\"#wtf\" style=\"font-size:4em\">?</div></center>");
    }});
    $.ajaxSetup({ async: false });

    var i = { 'stop': function () { } };
    $.getJSON("/poot", interpretation_arguments(filters), function (interpretation) {
        var content = target.find("#content");
        if (interpretation.type == "javascript") {
            $.ajaxSetup({ cache: false });
            $.ajaxSetup({ async: false });
            $.getScript(interpretation.content_location, function () {
                colorize(target);
                poot_title(target.find("#title"), interpretation);
                var p = pootpoot();
                p.start(content);
                i = p;
            });
        } else if (interpretation.type == "text") {
            $.ajaxSetup({ cache: false });
            $.ajaxSetup({ async: true });
            $.get(interpretation.content_location, function (data) {
                colorize(target);
                poot_title(target.find("#title"), interpretation);
                content.text(data);
                content.wrapInner("<pre></pre>");
            }, "text");
        } else if (interpretation.type == "html") {
            $.ajaxSetup({ cache: false });
            $.ajaxSetup({ async: true });
            $.get(interpretation.content_location, function (data) {
                colorize(target);
                poot_title(target.find("#title"), interpretation);
                content.html(data);
            }, "html");
        } else if (interpretation.type == "image") {
            colorize(target);
            poot_title(target.find("#title"), interpretation);
            var contents = "<center><img alt=\"" + interpretation.title + "\" src=\"" + interpretation.content_location + "\"/></center>";
            content.html(contents);
        }
    });

    return i;
}
