<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
<head>
 <title>poot poot interpretation list</title>
m4_include(common_header.m4)

 <style type="text/css">
.listed_interpretation {
  border-style: none none solid none
}

.page_link {
  padding: 5px;
}
 </style>

 <script type="text/javascript">
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

function pages (target, filters) {
    $.ajaxSetup({ cache: false });
    $.ajaxSetup({ error: function () {}});
    $.ajaxSetup({ async: false });
    $.getJSON("/list_pages", filters, function (page_list) {
        if (page_list.length > 1) {
            colorize(target);
            var contents = "Pages: ";
            for (var i in page_list) {
                contents += '<span class="page_link" id="page_link_' + page_list[i].page_number + '">[' + page_list[i].page_number + ']<span style="display: none" class="offset_key_string">' + page_list[i].offset_key_string + '</span></span>';
            }
            target.html(contents);
        }
    });
}

  $(function () {
   var filters = path_to_filters(unescape(document.location.href));

   colorize($("body"));
   pages($("#list_pages"), filters);
   list($("#list_interpretations"), filters);

   $(".page_link").click(function () {
       filters['offset_key_string'] = $(this).find(".offset_key_string").text();
       list($("#list_interpretations"), filters);
   });

   $("#list_interpretations").click(function (event) {
     colorize($("#list_interpretations"));
     shuffle_children($("#list_interpretations"));
     shuffle_children($("#buttons"));
     shuffle_children($("#bottom_links"));
   });
  });
 </script>
</head>

<body>
m4_include(buttons.m4)
 <div id="list_pages" class="main_content">
 </div>
 <div id="list_interpretations" class="main_content">
 </div>
m4_include(bottom_links.m4)
</body>

</html>
