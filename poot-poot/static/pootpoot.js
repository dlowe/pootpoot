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

function poot (target) {
    $.ajaxSetup({ cache: false });
    $.getJSON("/poot", function (json) {
        if (json.type == "javascript") {
            $.ajaxSetup({ cache: true });
            $.getScript(json.location, function (data, textStatus) {
                target.empty();
                target.css("background-color", random_color());
                pootpoot(target);
            });
        }
    });
}
