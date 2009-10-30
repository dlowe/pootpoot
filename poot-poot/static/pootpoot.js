// general, unit-testable, non-state-manipulating functions...
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

function shuffle (v) {
    for(var j, x, i = v.length; i; j = parseInt(Math.random() * i), x = v[--i], v[i] = v[j], v[j] = x);
    return v;
}

function path_to_filters (path) {
    var re      = new RegExp('/(?:a/([^/]+)/)?(?:t/([^/]+)/)?(?:ok/([^/]+)/)?(?:([^/]+).html)?$');
    var filters = {};
    if (re.test(path)) {
        var matches = re.exec(path);
        if (matches[1] != null) {
            filters['author'] = matches[1];
        }
        if (matches[2] != null) {
            filters['type'] = matches[2];
        }
        if (matches[3] != null) {
            filters['offset_key_string'] = matches[3];
        }
        if (matches[4] != null) {
            filters['title_link'] = matches[4];
        }
    }
    return filters;
}


// very general pooty randomizing functions which whack a specified jQuery target directly
function colorize (target) {
   target.css("background-color", random_color());
   target.css("color", random_color());
}

function shuffle_children (target) {
    var children          = target.children();
    var shuffled_elements = shuffle(children.get());
    target.empty();
    target.append(shuffled_elements);
}

function repaint () {
    $(".main_content").each(function () { colorize(jQuery(this)) });
    colorize($("body"));
    shuffle_children($("#buttons"));
    shuffle_children($("#bottom_links"));
    $("a").click(function (event) { event.stopPropagation(); });
}


// everything else in here is the code for displaying interpretations, tightly tied
// with interpretation.m4...
function expand_interpretation (target, interpretation) {
    target.find("#title_a").attr('href', interpretation.decorated_location);
    target.find("#interpretation_title").text(interpretation.title);
    target.find("#interpretation_author").text(interpretation.author);
    target.find("#author_a").attr('href', interpretation.author_location);
    target.find("#content_a").attr('href', interpretation.content_location);
    target.show();
}

var T_IMAGE      = 'image';
var T_TEXT       = 'text';
var T_HTML       = 'html';
var T_JAVASCRIPT = 'javascript';
var T_ALL        = [ T_IMAGE, T_TEXT, T_HTML, T_JAVASCRIPT ];
var TYPES = T_ALL.concat('error');
function show_content(content, show_type) {
    for (var i in TYPES) {
        if (TYPES[i] != show_type) {
            content.find("#content_" + TYPES[i]).hide();
        }
    }
    content.find("#content_" + show_type).show();
    return;
}

var global_this = (function(){return this;})();
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
        if (interpretation.type == T_JAVASCRIPT) {
            $.ajaxSetup({ cache: true });
            $.ajaxSetup({ async: false }); // or else assigning i=p does not work!
            $.getScript(interpretation.content_location, function () {
                target.unbind('click');
                colorize(target);
                expand_interpretation(target.find("#title"), interpretation);
                var p = global_this[interpretation.javascript_hook]();
                content.find("#content_javascript").empty();
                show_content(content, interpretation.type);
                p.start(content.find("#content_javascript"));
                i = p;
                ready();
            });
        } else if (interpretation.type == T_TEXT) {
            $.ajaxSetup({ cache: true });
            $.ajaxSetup({ async: true });
            $.get(interpretation.content_location, function (data) {
                target.unbind('click');
                colorize(target);
                expand_interpretation(target.find("#title"), interpretation);
                content.find("#content_text").text(data);
                show_content(content, interpretation.type);
                target.click(function () { repaint(); });
                ready();
            }, "text");
        } else if (interpretation.type == T_HTML) {
            $.ajaxSetup({ cache: true });
            $.ajaxSetup({ async: true });
            $.get(interpretation.content_location, function (data) {
                target.unbind('click');
                colorize(target);
                expand_interpretation(target.find("#title"), interpretation);
                content.find("#content_html").html(data);
                show_content(content, interpretation.type);
                target.click(function () { repaint(); });
                ready();
            }, "html");
        } else if (interpretation.type == T_IMAGE) {
            target.unbind('click');
            colorize(target);
            expand_interpretation(target.find("#title"), interpretation);
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
            target.click(function () { repaint(); });
            ready();
        }
    });

    return i;
}

// down here is pootifier code... incomplete
function pootify_word (word) {
    return 'poot';
}

function pootify_text (text) {
    return pootify_word(text);
}

function pootify_document (target) {
    for (l in target.childNodes) {
        var node = target.childNodes[l];
        if (node.nodeType == 3) {
            if (/\S/.test(node.nodeValue)) {
                node.parentNode.replaceChild(document.createTextNode(pootify_text(node.nodeValue)), node);
            }
        } else if (node.nodeType == 1)  {
            pootify_document(node);
        }
    }
    return;
}
