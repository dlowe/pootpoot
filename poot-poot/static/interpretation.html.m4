<!DOCTYPE html>
<html lang="en">
<head>
 <title>poot poot</title>
 <meta name="google-site-verification" content="wrrT2vJ0lSOQ6jY0YYun4Q4Dma7jXXDdWzjEtvoIJUU" />
 <link rel="alternate" type="application/rss+xml" title="poot poot" href="/feeds/interpretations/" />
m4_include(common_header.m4)

 <script type="text/javascript">
  function interpretationReady () {
      //colorize($("body"));
      repaint();
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
     if (filters['title_link'] == null) {
         $("#button_pootpoot").click(repoot);
     }
   };
   repoot(null);
  });
 </script>
</head>

<body>
m4_include(buttons.m4)
m4_include(interpretation.m4)
m4_include(bottom_links.m4)
</body>

</html>
