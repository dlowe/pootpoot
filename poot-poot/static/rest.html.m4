<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
<head>
 <title>pootpoot API documentation</title>
m4_include(common_header.m4)
 <style type="text/css">
#rest_docs {
  font-size: small;
}

.method_header {
  font-family: monospace;
}
 </style>
 <script type="text/javascript">
  $(function () {
   var repaint = function () {
       colorize($("body"));
       colorize($("#rest_docs"));
       shuffle_children($("#buttons"));
       shuffle_children($("#bottom_links"));
   };
   repaint();
   $("#rest_docs").click(repaint);
  });
 </script>
</head>

<body>
m4_include(buttons.m4)
 <div id="rest_docs" class="main_content">
 <p>
 If you're so inclined, you can access pootpoot data via the REST API.
 </p>
 <h2>Basics</h2>
 <p>Since nobody is using it and I'm moving pretty fast, this API is a moving target with no backwards compatibility guarantees.</p>
 <p>The API is HTTP-based; you interact through HTTP GET and POST requests.</p>
 <p>The API currently uses only JSON for serializing responses.</p>
 <p>Errors from any method are indicated both by a non-200 HTTP Response Code, and by the presence of an 'error' value in the returned JSON data. Either is sufficient to know that an error occurred.</p>

 <h2>Reading Interpretations</h2>
 <h3>Interpretation Filtering</h3>
 <p>
 All of the following methods accept a common set of parameters for filtering the interpretations
 under consideration. These parameters are:
 </p>
 <dl>
  <dt>key_string</dt>
   <dd>Opaque, unique identifier for a single interpretation. Main use within API is for submitting and manipulating interpretations. Using a specific key_string is the <em>only</em> way to read an inactive interpretation; using any other filter implicity causes the method to only consider active interpretations.</dd>
  <dt>title_link</dt>
   <dd>Human-consumable unique identifier for a single interpretation. This is the preferred method for fetching a specific interpretation and/or building permalinks.</dd>
  <dt>author</dt>
   <dd>The interpretation's author. Only interpretations matching this exact (case-sensitive) string are considered.</dd>
  <dt>offset_key_string</dt>
   <dd>A starting opaque key. Only interpretations whose key is &gt;= this value are considered. This is intended for use in pagination (see /list_pages and /list methods).</dd>
 </dl>

 <h3 class="method_header">/poot [GET]</h3>
 Given a set of filters, this returns <em>exactly one</em> interpretation, selected at random from the full set of matching interpretations, via an object containing:
  <dl>
   <dt>title</dt>
    <dd>Interpretation title</dd>
   <dt>author</dt>
    <dd>Interpretation author</dd>
   <dt>author_location</dt>
    <dd>URI (relative to the API host!) for more by this author.</dd>
   <dt>type</dt>
    <dd>The type of interpretation. One of: 'image', 'text', 'html', 'javascript'</dd>
   <dt>decorated_location</dt>
    <dd>Permalink URI (relative to the API host!) for fully decorated display of this interpretation.</dd>
   <dt>content_location</dt>
    <dd>URI (relative to the API host!) from which the content can be fetched.
  </dl>

 <h3 class="method_header">/count [GET]</h3>
 Given a set of filters, this returns a simple object containing the following:
  <dl>
   <dt>count</dt>
    <dd>Number of interpretations matched by the specified filters.</dd>
  </dl>

 <h3 class="method_header">/list_pages [GET]</h3>
 Given a set of filters, this returns a list of one or more objects, each of which contains the following:
  <dl>
   <dt>page_number</dt>
    <dd>Page number, starting from 1.</dd>
   <dt>offset_key_string</dt>
    <dd>Offset to pass as a filter to the /list to obtain the interpretations for the specified page.</dd>
  </dl>

 <h3 class="method_header">/list [GET]</h3>
 <p>
 See /list_pages above; these two methods need to be used together if you're trying to browse interpretations. Basically, you want to use /list_pages with your original filters, and then for each page use /list with the page's offset_key_string, returned by /list_pages, as an additional filter.
 </p>
 <p>
 Given a set of filters, this returns a list of 1 to 20 objects, each of which contains the following:
 </p>
 <dl>
  <dt>title</dt>
   <dd>Interpretation title</dd>
  <dt>author</dt>
   <dd>Interpretation author</dd>
  <dt>author_location</dt>
   <dd>URI (relative to the API host!) for more by this author.</dd>
  <dt>decorated_location</dt>
   <dd>Permalink URI (relative to the API host!) for fully decorated display of this interpretation.</dd>
 </dl>

 <h2>Writing Interpretations</h2>

 <h3 class="method_header">/submit [POST]</h3>
 <p>
 Create a new (inactive) interpretation. Requires the following input parameters:
 </p>
 <dl>
  <dt>title</dt>
   <dd>Interpretation title</dd>
  <dt>author</dt>
   <dd>Interpretation author</dd>
  <dt>type</dt>
   <dd>The type of interpretation. One of: 'image', 'text', 'html', 'javascript'</dd>
  <dt>content</dt>
   <dd>The content of the interpretation.</dd>
 </dl>
 <p>
 On success, returns an object containing the following:
 </p>
 <dl>
  <dt>key_string</dt>
   <dd>Opaque unique identifier for this interpretation, which can be used to retrieve the interpretation even if it remains inactive.</dd>
  <dt>owner_baton</dt>
   <dd>This is a password unique to the new interpretation. You will need an owner_baton to use any of the other writing methods!</dd>
  <dt>decorated_location</dt>
   <dd>Permalink URI (relative to the API host!) for fully decorated display of this interpretation. Note that this URI is not actually functional until the interpretation is active! XXX: should be returned by /approve instead, probably...</dd>
 </dl>

 <h3 class="method_header">/approve [POST]</h3>
 <p>Make a submitted interpretation active. Requires the following arguments:</p>
 <dl>
  <dt>key_string</dt>
   <dd>Opaque unique identifier for this interpretation. You saved it after calling /submit, right?</dd>
  <dt>owner_baton</dt>
   <dd>You saved it after calling /submit, right?</dd>
 </dl>
 <p>On success, returns an object containing the following:</p>
 <dl>
  <dt>ok</dt>
   <dt>ok</dt>
 </dl>
 
 <h3 class="method_header">/disapprove [POST]</h3>
 <p>Permanently delete a submitted interpretation. Requires the following arguments:</p>
 <dl>
  <dt>key_string</dt>
   <dd>Opaque unique identifier for this interpretation. You saved it after calling /submit, right?</dd>
  <dt>owner_baton</dt>
   <dd>You saved it after calling /submit, right?</dd>
 </dl>
 <p>On success, returns an object containing the following:</p>
 <dl>
  <dt>ok</dt>
   <dt>ok</dt>
 </dl>
 
 </div>
m4_include(bottom_links.m4)
</body>

</html>
