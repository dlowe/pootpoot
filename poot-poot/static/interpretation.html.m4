<!DOCTYPE html>
<html lang="en">
<head>
 <title>poot poot</title>
 <meta name="google-site-verification" content="wrrT2vJ0lSOQ6jY0YYun4Q4Dma7jXXDdWzjEtvoIJUU" />
 <link rel="alternate" type="application/rss+xml" title="poot poot" href="/feeds/interpretations/" />
m4_include(common_header.m4)

 <script type="text/javascript">
  function expand_comment(target, comment) {
      target.find('.comment_author').text(comment.author);
      target.find('.comment_created_at').text(comment.created_at);
      target.find('.comment_content').text(comment.content);
      target.show();
  }

  function interpretationReady (interpretation) {
      repaint();
      $("#link_show_comments").click(function () {
          target = $("#list_comments");
          $.ajaxSetup({ cache: false });
          $.ajaxSetup({ async: true });
          $.getJSON("/comment_list", {'interpretation_key_string': interpretation.key_string}, function (comment_list) {
              target.html(target.find("#comment_template"));
              colorize(target);
              for (var i in comment_list) {
                  var template = target.find("#comment_template").clone();
                  expand_comment(template, comment_list[i]);
                  target.append(template);
              }
              target.show();
          });
      });
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
 <div id="list_comments" class="main_content" style="display:none">
  <div class="comment" id="comment_template" style="display:none">
   <span class="comment_author">author</span>
   on <span class="comment_created_at">your birthday</span> said:<br>
   <span class="comment_content">Lorem ipsum dolor sit amet</span>
  </div>
 </div>
m4_include(bottom_links.m4)
</body>

</html>
