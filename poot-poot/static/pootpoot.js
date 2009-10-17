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
    target.find("#title_a").attr('href', interpretation.decorated_location);
    target.find("#interpretation_title").text(interpretation.title);
    target.find("#interpretation_author").text(interpretation.author);
    target.show();
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

function shuffle_buttons (target) {
    var children          = target.children();
    var shuffled_elements = shuffle(children.get());
    target.empty();
    target.append(shuffled_elements);
}

var TYPES = [ 'error', 'image', 'text', 'html', 'javascript' ];
function show_content(content, show_type) {
    for (var i in TYPES) {
        if (TYPES[i] != show_type) {
            content.find("#content_" + TYPES[i]).hide();
        }
    }
    content.find("#content_" + show_type).show();
    return;
}

function poot (target, filters, ready) {
    var content = target.find("#content");

    $.ajaxSetup({ cache: false });
    $.ajaxSetup({ error: function () {
        colorize(target);
        target.find("#title").hide();
        show_content(content, 'error');
    }});
    $.ajaxSetup({ async: false });

    var i = { 'stop': function () { } };
    $.getJSON("/poot", interpretation_arguments(filters), function (interpretation) {
        var content = target.find("#content");
        if (interpretation.type == "javascript") {
            $.ajaxSetup({ cache: false });
            $.ajaxSetup({ async: false }); // or else assigning i=p does not work!
            $.getScript(interpretation.content_location, function () {
                colorize(target);
                poot_title(target.find("#title"), interpretation);
                var p = pootpoot();
                content.find("#content_javascript").empty();
                show_content(content, interpretation.type);
                p.start(content.find("#content_javascript"));
                i = p;
                ready();
            });
        } else if (interpretation.type == "text") {
            $.ajaxSetup({ cache: false });
            $.ajaxSetup({ async: true });
            $.get(interpretation.content_location, function (data) {
                colorize(target);
                poot_title(target.find("#title"), interpretation);
                content.find("#content_text").text(data);
                show_content(content, interpretation.type);
                ready();
            }, "text");
        } else if (interpretation.type == "html") {
            $.ajaxSetup({ cache: false });
            $.ajaxSetup({ async: true });
            $.get(interpretation.content_location, function (data) {
                colorize(target);
                poot_title(target.find("#title"), interpretation);
                content.find("#content_html").html(data);
                show_content(content, interpretation.type);
                ready();
            }, "html");
        } else if (interpretation.type == "image") {
            colorize(target);
            poot_title(target.find("#title"), interpretation);
            var img = content.find("#content_image").find("img");
            // to avoid UI warping the old image to new dimensions while the new image loads
            img.attr({
                'src': ''
            });
            img.attr({
                'height': interpretation.image_height,
                'width':  interpretation.image_width,
                'src':    interpretation.content_location,
                'alt':    interpretation.title,
                'title':  interpretation.title
            });
            show_content(content, interpretation.type);
            ready();
        }
    });

    return i;
}
