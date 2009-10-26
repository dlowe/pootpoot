<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
<head>
 <title>submit to poot poot</title>
m4_include(common_header.m4)
 <script type="text/javascript">

function change_details () {
    var show_type = $("input[name='type']:checked").val();
    for (var i in T_ALL) {
        if (T_ALL[i] != show_type) {
            $("#details_" + T_ALL[i]).hide();
        }
    }
    $("#details_" + show_type).show();

    colorize($("#submit_details"));
    shuffle_children($("#buttons"));
    shuffle_children($("#bottom_links"));
    return;
}

  $(function () {
   colorize($("body"));
   colorize($("#submit_details"));
   shuffle_children($("#buttons"));
   shuffle_children($("#bottom_links"));

   $("#submit_form").ajaxForm({
       "iframe": true,
       "dataType": 'json',
       "success": function (json) {
           if (json.error != null) {
               $("#submit_error_text").text(json.error);
               $("#submit_error").show();
               return;
           }

           $("#submit_error").hide();
           $("#good").click(function (eventObject) {
               eventObject.preventDefault();
               var arguments = { 'key_string': json.key_string, 'owner_baton': json.owner_baton };
               $.ajaxSetup({ cache: false });
               $.ajaxSetup({ dataType: 'json' });
               $.post("/approve", arguments, function (interpretation) {
                   window.location = interpretation.decorated_location;
               });
           });

           $("#bad").click(function (eventObject) {
               eventObject.preventDefault();
               var arguments = { 'key_string': json.key_string, 'owner_baton': json.owner_baton };
               $.ajaxSetup({ cache: false });
               $.ajaxSetup({ dataType: 'json' });
               $.post("/disapprove", arguments, function (interpretation) {
               });
               $("#pending").hide();
               $("#submit_details").show();
           });

           $("#submit_details").hide()
           $("#pending").show()
           poot($("#interpretation"), { 'key_string': json.key_string }, function () { });
       }
   });
  });
 </script>
</head>

<body>
m4_include(buttons.m4)
 <div id="submit_details" class="main_content">
 <div id="submit_details_header">
  Use this form to submit your own interpretation of Poot.
 </div>
 <table style="width: 90%; table-layout: fixed"><tr>
 <td style="width: 60%; vertical-align: top">
 <form id="submit_form" action="/submit" method="post" enctype="multipart/form-data" style="margin-top: 0px">
   <table>
    <tr><td>title:</td><td><input type="text" name="title"></td></tr>
    <tr><td>author:</td><td><input type="text" name="author"></td></tr>
    <tr><td>type:</td><td>
     <input type="radio" name="type" value="image" onChange="change_details();">image
     <input type="radio" name="type" value="text" onChange="change_details();">text
     <input type="radio" name="type" value="html" onChange="change_details();">html
     <input type="radio" name="type" value="javascript" onChange="change_details();">javascript
   </td></tr>
   <tr><td>content:</td><td><input type="file" name="content"></td></tr>
   </table>
   <div><input type="submit" value="poot"></div>
 </form>
 </td>
 <td style="width: 40%">
  <div id="submit_error" style="display: none">
   <p>Problem: <span id="submit_error_text"></span></p>
  </div>

  <div id="details_image" style="display: none">
   <p>
   Pooty picture in .gif, .jpg or .png format. Images must be smaller than 900x900 pixels and less than 1MB file size.
   </p>

   <p>
   Image interpretations are displayed unchanged, centered in the page.
   </p>

   <p>
   Example: <a href="/interpretation/poot-pie.html">Poot Pie</a>
   </p>
  </div>

  <div id="details_text" style="display: none">
   <p>
   Pooty plain text.
   </p>

   <p>
   Text interpretations are displayed in fixed-width font, and the whitespace and newlines of the input file are retained.
   </p>

   <p>
   Example: <a href="/interpretation/poot-c.html">poot.c</a>
   </p>
  </div>

  <div id="details_html" style="display: none">
   <p>
   Pooty HTML fragment. Your input HTML will be liberally mangled to prevent abuse; basically anything beyond basic formatting markup is verboten.
   </p>

   <p>
   HTML interpretations are just mashed into the page. Exciting!
   </p>

   <p>
   Example: <a href="/interpretation/what.html">What?</a>
   </p>
  </div>

  <div id="details_javascript" style="display: none">
   <p>
   Pooty plugin written in javascript. Input javascript is checked for safety. Sorta.
   </p>

   <p>
   Javascript interpretations must include a function pootpoot(), which returns an object with two methods: start() and stop(). The start() method will be called with a single jQuery object argument, which refers to the area on the page your script can manipulate at will. The stop() method will be called with no arguments when the code should stop and clean up.
   </p>

   <p>
   Example: <a href="/interpretation/original-poot.html">The Original Poot</a> (and the <a href="/i/aglwb290LXBvb3RyFAsSDkludGVycHJldGF0aW9uGAUM">plugin code</a>)
   </p>
  </div>
 </td>
 </tr></table>
 </div>

 <div id="pending" style="display: none">
 <div class="main_content">
  Here's what I got. How's it look? <a id="good" href="">good</a> <a id="bad" href="">bad</a><br>
 </div>
m4_include(interpretation.m4)
 </div>

m4_include(bottom_links.m4)
</body>

</html>
