<!DOCTYPE html>
<html lang="en">
<head>
 <title>poot poot</title>
 <meta name="google-site-verification" content="wrrT2vJ0lSOQ6jY0YYun4Q4Dma7jXXDdWzjEtvoIJUU" />
 <link rel="alternate" type="application/rss+xml" title="poot poot" href="/feeds/interpretations/" />
m4_include(common_header.m4)

 <style type="text/css">
.comment {
  border-bottom-width: 1px;
  border-bottom-style: dotted;
}

.comment_header {
  font-size: 0.8em;
  font-weight: bold;
}

.comment_body {
  font-size: 0.9em;
  margin-left: 8px;
}

.comment_footer {
  font-size: 0.6em;
}

#comment_error {
  font-size: 1.1em;
  color: red;
}
 </style>

 <script type="text/javascript">
  function expand_comment(target, comment) {
      target.find('.comment_author').text(comment.author);
      target.find('.comment_created_at').text(comment.created_at);
      target.find('.comment_content').text(comment.content);
      target.show();
  }

  function interpretationReady (interpretation) {
      repaint();

      $("#interpretation_key_string").attr('value', interpretation.key_string);

      $("#link_add_comment").click(function (event) {
          event.preventDefault();
          $("#add_comment").show();
          $("#form_author").focus();
      });
      $(".add_comments").show();

      $("#link_show_comments").click(function (event) {
          event.preventDefault();
          target = $("#list_comments");
          $.ajaxSetup({ cache: false });
          $.ajaxSetup({ async: true });
          $.ajaxSetup({ error: null });
          $.getJSON("/comment_list", {'interpretation_key_string': interpretation.key_string}, function (comment_list) {
              target.html(target.find("#comment_template"));
              colorize(target);
              for (var i in comment_list) {
                  var template = target.find("#comment_template").clone();
                  template.attr('id', "comment_" + i);
                  expand_comment(template, comment_list[i]);
                  target.append(template);
              }
              target.show();
          });
      });
  }
  $(function () {
   var filters = path_to_filters(unescape(document.location.href));

   $("#comment_form").ajaxForm({
       "iframe": true,
       "dataType": 'json',
       "success": function (json) {
           if (json.error != null) {
               $("#comment_error_text").text(json.error);
               $("#comment_error").show();
               return;
           }

           $("#comment_error").hide();
           $("#link_show_comments").click();
           $("#form_author").attr('value', '');
           $("#form_content").val('');
           $("#add_comment").hide();
       }
   });

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
 <div id="list_comments" class="main_content" style="display:none">
  <div id="comment_template" class="comment" style="display:none">
   <div class="comment_header"><span class="comment_author">author</span> said...</div>
   <div class="comment_body"><pre><span class="comment_content">Lorem ipsum dolor sit amet</span></pre></div>
   <div class="comment_footer"><span class="comment_created_at">your birthday</span></div>
  </div>
 </div>

 <div id="add_comment" class="main_content" style="display:none">
  <form id="comment_form" action="/comment_submit" method="post" enctype="multipart/form-data">
  <table style="table-layout: fixed" summary="comment submission form and help">
  <tr><td style="width: 60%; vertical-align: top">
   <table summary="comment submission form">
    <tr><td>your name:</td><td><input id="form_author" type="text" name="author"></td></tr>
    <tr><td>your comment:</td><td><textarea id="form_content" name="content" cols=40 rows=10></textarea></td></tr>
   </table>
   <div>
    <input id="interpretation_key_string" type="hidden" name="interpretation_key_string" value="fnord">
    <input type="submit" value="poot">
   </div>
   </td>
   <td style="width: 40%">
    <div id="comment_error" style="display: none">
     <p>Problem: <span id="comment_error_text"></span></p>
    </div>
   </td></tr>
  </table>
  </form>
 </div>
m4_include(bottom_links.m4)
</body>

</html>
