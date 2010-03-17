<!DOCTYPE html>
<html lang="en">
<head>
 <title>pootify all web pages!</title>
m4_include(common_header.m4)
 <style type="text/css">
#pootify_text {
  text-align: center;
  margin: 0px auto;
}
 </style>

 <script type="text/javascript">
  $(function () {
   repaint();
   $("#pootify").click(repaint);
  });
 </script>
</head>

<body>
m4_include(buttons.m4)
 <div id="pootify" class="main_content">
 <div id="pootify_text">

 <p>Pootify all web pages!</p>
 <p>See the world wide web as it was truly meant to be seen!</p>

 <form action="/pootify" method="get">
  <input type="text" name="url" value="http://" size=50><br>
  <input type="submit" value="POOTIFY!">
 </form>

 </div>
 </div>
m4_include(bottom_links.m4)
</body>

</html>
