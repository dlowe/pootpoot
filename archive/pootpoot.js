function pootpoot () {
var poot_styles = [
  {one_in: 15, style: "text-decoration:underline"},
  {one_in: 30, style: "text-decoration:line-through"},
  {one_in: 40, style: "text-decoration:blink"},
  {one_in: 10, style: "font-weight:bold"},
  {one_in: 6,  style: "text-transform:uppercase"},
  {one_in: 4,  style: "text-transform:capitalize"},
  {one_in: 11, style: "font-style:italic"}
];

function _pootpoot (target) {
    target.empty();
    target.unbind('click');
    target.click(function () { _pootpoot(target); });
    var line_count = r(1, 40);
    for (var i = 0; i < line_count; ++i) {
        var alignment = ["center", "left", "right"][r(0, 2)];

        var line = '<div style="text-align:' + alignment + ';">';

        var poot_count = r(1, 8);
        for (var j = 0; j < poot_count; ++j) {
            var poot = '<font style="color:' + random_color() + ";font-size:" + ((Math.random() * 2) + 0.2) + "em";
            for (var s in poot_styles) {
                if (r(1, poot_styles[s].one_in) == 1) {
                    poot += ";" + poot_styles[s].style;
                }
            }
            poot += '">';
            if (r(0, 4) == 0) {
                poot += "poot";
            }
            poot += "poot</font>";
            var space_count = r(0, 18);
            for (var k = 0; k < space_count; ++k) {
                poot += "&nbsp;";
            }

            line += poot;
        }
        line += "</div><br/>";
        target.append(line);
    }
    return;
}

return {
    'start': function (target) { _pootpoot(target) },
    'stop':  function () { }
};
}
