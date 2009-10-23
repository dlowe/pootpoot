<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
<head>
 <title>poot poot interpretation list</title>
m4_include(common_header.m4)

 <style type="text/css">
#list_interpretations {
  margin: 0px auto;
  width: 90%;
  padding: 10px;
  overflow: hidden;
}

.listed_interpretation {
  border-style: none none solid none
}
 </style>

 <script type="text/javascript">
  $(function () {
   var filters = path_to_filters(unescape(document.location.href));

   colorize($("body"));
   list($("#list_interpretations"), filters);
   shuffle_buttons($("#buttons"));
   $("html").click(function (event) {
     list($("#list_interpretations"), filters);
     shuffle_buttons($("#buttons"));
   });
  });
 </script>
</head>

<body>
 <div id="list_interpretations">
 </div>
m4_include(buttons.m4)
</body>

</html>
