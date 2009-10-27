<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
<head>
 <title>what?</title>
m4_include(common_header.m4)
 <script type="text/javascript">
  $(function () {
   var repaint = function () {
       colorize($("body"));
       colorize($("#what"));
       shuffle_children($("#buttons"));
       shuffle_children($("#bottom_links"));
   };
   repaint();
   $("#what").click(repaint);
  });
 </script>
</head>

<body>
m4_include(buttons.m4)
 <div id="what" class="main_content">

 <h2>Welcome to Poot Poot!</h2>
 <p>
 Poot means many things to many people, but our goal is simple: To showcase web wide interpretations of Poot. <a href="/submit.html">Submit</a> your interpretation of Poot and it will be connected to other Poots for all to see and appreciate!
 </p>
 </div>
m4_include(bottom_links.m4)
</body>

</html>
