<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
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
   var repaint = function () {
       colorize($("body"));
       colorize($("#code"));
       shuffle_children($("#buttons"));
       shuffle_children($("#bottom_links"));
   };
   repaint();
   $("#code").click(repaint);
  });
 </script>
</head>

<body>
m4_include(buttons.m4)
 <div id="code" class="main_content">
 <p>
 pootpoot is open-source software. You can follow the project <a href="http://www.assembla.com/spaces/pootpoot/new_items">here</a>, browse the source <a href="http://trac-hg.assembla.com/pootpoot/browser">here</a>, and keep tabs on what I'm doing next <a href="http://trac-hg.assembla.com/pootpoot/report/1">here</a>. I'd love help if you're interested!
 </p>

 <p>
 The following are some of the bits and pieces from which this is cobbled together:
 </p>

 <dl>
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
  <dt><a href="http://mercurial.selenic.com/wiki/">mercurial</a></dt>
   <dd>source control</dd>
  <dt><a href="http://trac.edgewall.org/">trac</a></dt>
   <dd>defect and work tracking</dd>
  <dt><a href="http://www.assembla.com/">assembla</a></dt>
   <dd>trac and mercurial hosting</dd>
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
