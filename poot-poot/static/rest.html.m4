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
 <p>The API is HTTP-based; you interact through HTTP GET (for querying) and POST (for modifying) requests.</p>
 <p>The API currently uses only JSON for serializing responses.</p>
 <p>Errors from any method are indicated both by a non-200 HTTP Response Code, and by the presence of an 'error' value in the returned JSON data. Either is sufficient to know that an error occurred.</p>

 <h2>Interpretations</h2>
 <h3><a name="interpretation_object">Interpretation Objects</a></h3>
 <p>Many of the interpretation API methods below return serialized interpretation data, which are objects consisting of:</p>
 <dl>
  <dt>title</dt>
   <dd>Title of the interpretation</dd>
  <dt>author</dt>
   <dd>Author of the interpretation</dd>
  <dt>type</dt>
   <dd>Type of the interpretation (one of 'image', 'text', 'html', 'javascript')</dd>
  <dt>content_location</dt>
   <dd>URL (relative to the API host) where the interpretation's contents can be downloaded</dd>
  <dt>author_location</dt>
   <dd>URL (relative to the API host) where information about the author can be found</dd>
  <dt>decorated_location</dt>
   <dd>URL (relative to the API host) where the interpretation can be viewed</dd>
 </dl>
 <h3><a name="filter_parameters">Filter Parameters</a></h3>
 <p>
 Many of the interpretation API methods below accept a common set of parameters for filtering the interpretations
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

 <h3 class="method_header"><a name="method_poot">/poot [GET]</a></h3>
 <p>Given a set of <a href="#filter_parameters">filter parameters</a>, this returns <em>exactly one</em> <a href="#interpretation_object">interpretation object</a>, selected at random from the full set of matching interpretations.</p>

 <h3 class="method_header"><a name="method_count">/count [GET]</a></h3>
 <p>Given a set of <a href="#filter_parameters">filter parameters</a>, this returns a simple object containing the following:</p>
  <dl>
   <dt>count</dt>
    <dd>Number of interpretations matched by the specified filters.</dd>
  </dl>

 <h3 class="method_header"><a name="method_list_pages">/list_pages [GET]</a></h3>
 <p>Given a set of <a href="#filter_parameters">filter parameters</a>, this returns a list of one or more objects, each of which contains the following:</p>
  <dl>
   <dt>page_number</dt>
    <dd>Page number, starting from 1.</dd>
   <dt>offset_key_string</dt>
    <dd>Offset to pass as in the <a href="#filter_parameters">filter parameters</a> to the <a href="#method_list">/list method</a> to obtain the interpretations for the specified page.</dd>
  </dl>

 <h3 class="method_header"><a name="method_list">/list [GET]</a></h3>
 <p>Given a set of <a href="#filter_parameters">filter parameters</a>, this returns a list of 1 to 20 <a href="#interpretation_object">interpretation objects</a>.</p>
 <p>
 See the <a href="#method_list_pages">/list_pages method</a> above; these two methods need to be used together if you're trying to browse interpretations. Basically, you want to call /list_pages with the desired filters. For each returned page, call /list with the page's offset_key_string (returned by /list_pages), as a filter in addition to the originals.
 </p>

 <h3 class="method_header"><a name="method_submit">/submit [POST]</a></h3>
 <p>Create a new (inactive) interpretation. Requires the following input parameters:</p>
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
 <p>On success, returns an object containing the following:</p>
 <dl>
  <dt>key_string</dt>
   <dd>Opaque unique identifier for this interpretation, which can be used to retrieve the interpretation even if it remains inactive.</dd>
  <dt>owner_baton</dt>
   <dd>This is a password unique to the new interpretation. You will need an owner_baton to use any of the other writing methods!</dd>
 </dl>

 <h3 class="method_header"><a name="method_approve">/approve [POST]</a></h3>
 <p>Make a submitted interpretation active. Requires the following arguments:</p>
 <dl>
  <dt>key_string</dt>
   <dd>Opaque unique identifier for this interpretation. You saved it after calling /submit, right?</dd>
  <dt>owner_baton</dt>
   <dd>You saved it after calling the <a href="#method_submit">/submit method</a>, right?</dd>
 </dl>
 <p>On success, returns the approved <a href="#interpretation_object">interpretation object</a>.</p>
 
 <h3 class="method_header"><a name="method_disapprove">/disapprove [POST]</a></h3>
 <p>Permanently delete a submitted interpretation. Requires the following arguments:</p>
 <dl>
  <dt>key_string</dt>
   <dd>Opaque unique identifier for this interpretation. You saved it after calling /submit, right?</dd>
  <dt>owner_baton</dt>
   <dd>You saved it after calling the <a href="#method_submit">/submit method</a>, right?</dd>
 </dl>
 <p>On success, returns the deleted <a href="#interpretation_object">interpretation object</a>.</p>
 
 </div>
m4_include(bottom_links.m4)
</body>

</html>
