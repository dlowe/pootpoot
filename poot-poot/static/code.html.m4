<!DOCTYPE html>
<html lang="en">
<head>
 <title>pootpoot code</title>
m4_include(common_header.m4)
 <style type="text/css">
#code {
  font-size: small;
}
 </style>
 <script type="text/javascript">
  $(function () {
   repaint();
   $("#code").click(repaint);
  });
 </script>
</head>

<body>
m4_include(buttons.m4)
 <div id="code" class="main_content">
 <p>
 pootpoot is open-source software. You can follow the project and browse the source <a href="http://github.com/dlowe/pootpoot">here</a>, and keep tabs on what I'm doing next <a href="http://github.com/dlowe/pootpoot/issues">here</a>. I'd love help if you're interested!
 </p>

 <p>
 The following are some of the bits and pieces from which this is cobbled together:
 </p>

 <dl>
  <dt><a href="http://web.archive.org/">The Wayback Machine</a></dt>
   <dd>recovering scads of 10-year-old content</dd>
  <dt><a href="http://code.google.com/appengine/">Google App Engine</a></dt>
   <dd>hosting, data storage, image manipulation</dd>
  <dt><a href="http://python.org/">Python</a></dt>
   <dd>server code</dd>
  <dt><a href="http://feedparser.org/">feedparser</a></dt>
   <dd>HTML sanitizing</dd>
  <dt><a href="http://code.google.com/p/pynarcissus/">pynarcissus</a></dt>
   <dd>server-side javascript parsing</dd>
  <dt><a href="http://jquery.com/">jQuery</a></dt>
   <dd>javascript minus much of the pain</dd>
  <dt><a href="http://jquery.malsup.com/form/">jQuery form plugin</a></dt>
   <dd>AJAXy forms</dd>
  <dt><a href="http://www.openjs.com/scripts/events/keyboard_shortcuts/">shortcuts.js</a></dt>
   <dd>javascript keyboard shortcuts</dd>
  <dt><a href="http://www.github.com/">github</a></dt>
   <dd>code and issue hosting</dd>
  <dt><a href="http://www.gnu.org/software/m4/">m4</a></dt>
   <dd>template expansion</dd>
  <dt><a href="http://somethingaboutorange.com/mrl/projects/nose/0.11.1/">nose</a> and <a href="http://code.google.com/p/nose-gae/">nose-gae</a></dt>
   <dd>testing server code</dd>
  <dt><a href="http://www.logilab.org/857/">pylint</a></dt>
   <dd>static analysis of server code</dd>
  <dt><a href="http://wiki.github.com/berke/jsure">jsure</a></dt>
   <dd>static analysis of javascript code</dd>
 </dl>
 </div>
m4_include(bottom_links.m4)
</body>

</html>
