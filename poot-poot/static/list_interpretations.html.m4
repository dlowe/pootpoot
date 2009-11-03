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

#list_error {
  text-align: center;
  margin: 0px auto;
  font-size: 4em;
}
 </style>

 <script type="text/javascript">
var INTERPRETATIONS_PER_PAGE = 16;

function list (target, filters) {
    $.ajaxSetup({ cache: false });
    $.ajaxSetup({ error: function () {
        colorize(target);
        target.find("#list_error").show();
    }});
    $.getJSON("/list", filters, function (interpretation_list) {
        target.html(target.find("#listed_interpretation_template"));
        colorize(target);
        var shuffled_list = shuffle(interpretation_list);
        for (var i in shuffled_list) {
            var template = target.find("#listed_interpretation_template").clone();
            template.attr('id', "listed_interpretation_" + i);
            expand_interpretation(template, shuffled_list[i]);
            target.append(template);
        }
    });
}

function pages (target, base_filters) {
    $.ajaxSetup({ cache: false });
    $.ajaxSetup({ error: function () {}});
    $.ajaxSetup({ async: false });

    var page_filters = [];
    $.getJSON("/list_pages", base_filters, function (page_list) {
        for (var i in page_list) {
            page_filters[i] = { 'offset_key_string': page_list[i].offset_key_string };
            for (var key in base_filters) {
                page_filters[i][key] = base_filters[key];
            }
        }
        if (page_list.length > 1) {
            colorize(target);
            for (var i in page_list) {
                var template = target.find("#page_link_template").clone();
                template.attr('id', "page_link_" + page_list[i].page_number);
                template.find(".page_number").text(page_list[i].page_number);
                template.show();
                target.append(template);
            }
            target.show();
        }
    });
    return page_filters;
}

  $(function () {
   var base_filters = path_to_filters(unescape(document.location.href));
   base_filters['items'] = INTERPRETATIONS_PER_PAGE;

   var page_filters = pages($("#list_pages"), base_filters);
   list($("#list_interpretations"), page_filters[0]);
   repaint();

   $(".page_link").click(function () {
       var page = $(this).find(".page_number").text();
       list($("#list_interpretations"), page_filters[page - 1]);
       repaint();
   });

   $("#list_interpretations").click(function (event) {
     shuffle_children($("#list_interpretations"));
     repaint();
   });
  });
 </script>
</head>

<body>
m4_include(buttons.m4)
 <div id="content_error" class="main_content" style="display:none">
 </div>
 <div id="list_pages" class="main_content" style="display:none">
  Pages: 
  <span class="page_link" id="page_link_template" style="display:none">
   [<span class="page_number"></span>]
  </span>
 </div>
 <div id="list_interpretations" class="main_content">
  <div id="list_error" style="display:none">?</div>
  <div class="listed_interpretation" id="listed_interpretation_template" style="display:none">
   <a id="title_a"><span id="interpretation_title"></span></a>
   by <a id="author_a"><span id="interpretation_author"></span></a>
  </div>
 </div>
m4_include(bottom_links.m4)
</body>

</html>
