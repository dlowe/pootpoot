<!-- begin common_header.m4 -->
<meta http-equiv="Content-Type" content="text/html;charset=utf-8">

<link rel="icon" type="image/vnd.microsoft.icon" href="/favicon.ico">
<link rel="stylesheet" type="text/css" href="/pootpoot.css">

<script type="text/javascript" src="/jquery-1.3.2.min.js"></script>
<script type="text/javascript" src="/jquery.form.js"></script>
<script type="text/javascript" src="/shortcuts.js"></script>
<script type="text/javascript" src="/pootpoot.js"></script>

m4_ifdef(`POOTPOOT_ANALYTICS_KEY',
<script type="text/javascript">
var gaJsHost = (("https:" == document.location.protocol) ? "https://ssl." : "http://www.");
document.write(unescape("%3Cscript src='" + gaJsHost + "google-analytics.com/ga.js' type='text/javascript'%3E%3C/script%3E"));
</script>
<script type="text/javascript">
try {
var pageTracker = _gat._getTracker('POOTPOOT_ANALYTICS_KEY');
pageTracker._trackPageview();
} catch(err) {}</script>
)

<script type="text/javascript">
$(function () {
    colorize($("body"));
    shortcut.add('P', function () { pootify_document(document.body); }, { 'disable_in_input': true });
});
</script>

<!-- end common_header.m4 -->
