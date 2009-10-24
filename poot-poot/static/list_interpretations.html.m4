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
     shuffle_buttons($("#list_interpretations"));
     shuffle_buttons($("#buttons"));
   });
  });
 </script>
</head>

<body>
 <div id="list_pages" class="main_content">
 </div>
 <div id="list_interpretations" class="main_content">
 </div>
m4_include(buttons.m4)
</body>

</html>
