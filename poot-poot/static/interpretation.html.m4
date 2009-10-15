<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
<head>
m4_include(common_header.m4)

 <script type="text/javascript">
  function interpretationReady () {
      colorize($("body"));
  }
  $(function () {
   var re         = new RegExp('/interpretation/([^/]+).html$');
   var title_link = null;
   if (re.test(document.location.href)) {
       title_link = (re.exec(document.location.href))[1];
   }
   shuffle_buttons($("#buttons"));
   var interpretation = poot($("#interpretation"), { 'title_link': title_link }, interpretationReady);
   $("#button_pootpoot").click(function (event) {
     event.preventDefault();
     interpretation.stop();
     interpretation = poot($("#interpretation"), { 'title_link': title_link }, interpretationReady);
     shuffle_buttons($("#buttons"));
   });
  });
 </script>
</head>

<body>
m4_include(interpretation.m4)
m4_include(buttons.m4)
</body>

</html>
