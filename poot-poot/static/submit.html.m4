<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
<head>
m4_include(common_header.m4)
 <script type="text/javascript">
  $(function () {
   colorize($("body"));
   shuffle_buttons($("#buttons"));
   $("#submit_form").ajaxForm({
       "iframe": true,
       "dataType": null,
       "success": function (json) {
           //XXX: having a hard time getting json to auto-parse here, so whack it with a regex or 3...
           var key_re = new RegExp('"key":"([^"]*)"');
           var key = key_re.exec(json)[1];
           var owner_baton_re = new RegExp('"owner_baton":"([^"]*)"');
           var owner_baton = owner_baton_re.exec(json)[1];
           var decorated_location_re = new RegExp('"decorated_location":"([^"]*)"');
           var decorated_location = decorated_location_re.exec(json)[1];

           $("#good").click(function (eventObject) {
               eventObject.preventDefault();
               var arguments = { 'key': key, 'owner_baton': owner_baton };
               $.ajaxSetup({ cache: false });
               $.get("/approve", arguments, function () {
                   window.location = decorated_location;
               });
           });

           $("#bad").click(function (eventObject) {
               eventObject.preventDefault();
               var arguments = { 'key': key, 'owner_baton': owner_baton };
               $.ajaxSetup({ cache: false });
               $.get("/disapprove", arguments, function () {
               });
               $("#pending").hide();
               $("#submit_form").show();
           });

           poot($("#interpretation"), { 'key_string': key }, function () { });
           $("#submit_form").hide()
           $("#pending").show()
       }
   });
  });
 </script>
</head>

<body>
 <form id="submit_form" action="/submit" method="post" enctype="multipart/form-data">
   <div>title: <input type="text" name="title"></div>
   <div>author: <input type="text" name="author"></div>
   <div>type: <input type="text" name="type"></div>
   <div>content: <input type="file" name="content"></div>
   <div><input type="submit" value="poot"></div>
 </form>

 <div id="pending" style="display: none">
  Here's what I got. How's it look? <a id="good" href="">good</a> <a id="bad" href="">bad</a><br>
m4_include(interpretation.m4)
 </div>

m4_include(buttons.m4)
</body>

</html>
