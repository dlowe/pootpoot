<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
<head>
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
   var re         = new RegExp('/list_interpretations/([^/]+).html$');
   var title_link = null;
   if (re.test(document.location.href)) {
       title_link = (re.exec(document.location.href))[1];
   }
   colorize($("body"));
   list($("#list_interpretations"), { 'title_link': title_link })
   $("html").click(function (event) {
     list($("#list_interpretations"), { 'title_link': title_link })
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
