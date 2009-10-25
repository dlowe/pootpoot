<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
<head>
 <title>poot poot</title>
m4_include(common_header.m4)

 <script type="text/javascript">
  function interpretationReady () {
      colorize($("body"));
  }
  $(function () {
   var filters = path_to_filters(unescape(document.location.href));

   var interpretation = null;
   var repoot = function (event) {
     if (event != null) {
         event.preventDefault();
     }
     if (interpretation != null) {
         interpretation.stop();
     }
     interpretation = poot($("#interpretation"), filters, interpretationReady);
     shuffle_buttons($("#buttons"));
     if (filters['title_link'] == null) {
         $("#button_pootpoot").click(repoot);
     }
   };
   repoot(null);
  });
 </script>
</head>

<body>
m4_include(interpretation.m4)
m4_include(buttons.m4)
</body>

</html>
