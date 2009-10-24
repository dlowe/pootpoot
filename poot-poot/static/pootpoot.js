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
    target.find("#author_a").attr('href', interpretation.author_location);
    target.show();
}

function path_to_filters (path) {
    var re      = new RegExp('/(?:a/([^/]+)/)?(?:ok/([^/]+)/)?(?:([^/]+).html)?$');
    var filters = {};
    if (re.test(path)) {
        var matches = re.exec(path);
        if (matches[1] != null) {
            filters['author'] = matches[1];
        }
        if (matches[2] != null) {
            filters['offset_key_string'] = matches[2];
        }
        if (matches[3] != null) {
            filters['title_link'] = matches[3];
        }
    }
    return filters;
}

function pages (target, filters) {
    $.ajaxSetup({ cache: false });
    $.ajaxSetup({ error: function () {}});
    $.ajaxSetup({ async: false });
    $.getJSON("/list_pages", filters, function (page_list) {
        if (page_list.length > 0) {
            colorize(target);
            var contents = "Pages: ";
            for (var i in page_list) {
                contents += '<span class="page_link" id="page_link_' + page_list[i].page_number + '">[' + page_list[i].page_number + ']<span style="display: none" class="offset_key_string">' + page_list[i].offset_key_string + '</span></span>';
            }
            target.html(contents);
        }
    });
}

function list (target, filters) {
    $.ajaxSetup({ cache: false });
    $.ajaxSetup({ error: function () {}});
    $.getJSON("/list", filters, function (interpretation_list) {
        colorize(target);
        var contents = "";
        var shuffled_list = shuffle(interpretation_list);
        for (var i in shuffled_list) {
            contents += "<div class=\"listed_interpretation\"><a href=\"" + shuffled_list[i].decorated_location + "\">" + shuffled_list[i].title + "</a> by <a href=\"" + shuffled_list[i].author_location + "\">" + shuffled_list[i].author + "</a></div>"
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
    $.getJSON("/poot", filters, function (interpretation) {
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
