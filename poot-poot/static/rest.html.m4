<!DOCTYPE html>
<html lang="en">
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

.doc_block {
  position: relative;
  left: 20px;
}
 </style>
 <script type="text/javascript">
  $(function () {
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
 <h2>The Basics</h2>
 <p>Since nobody is using it and I'm working pretty fast, this API is a moving target with no backwards compatibility guarantees.</p>
 <p>The API is HTTP-based; you interact through HTTP GET (for querying) and POST (for modifying) requests.</p>
 <p>The API currently uses only JSON for serializing responses.</p>
 <p>Errors from any method are indicated both by a non-200 HTTP Response Code, and by the presence of an 'error' value in the returned JSON data. Either is sufficient to know that an error occurred.</p>

 <h2>Interpretations</h2>
 <h3><a name="interpretation_object">Interpretation Objects</a></h3>
 <div class="doc_block">
 <p>Many of the interpretation API methods below return serialized interpretation data, which are objects consisting of:</p>
 <dl>
  <dt>key_string</dt>
   <dd>Unique key identifying this interpretation</dd>
  <dt>title</dt>
   <dd>Title of the interpretation</dd>
  <dt>author</dt>
   <dd>Author of the interpretation</dd>
  <dt>created_at</dt>
   <dd>Formatted date string (%a, %d %b %Y %H:%M:%S GMT) when this interpretation was created</dd>
  <dt>is_active</dt>
   <dd>Boolean indicating whether this interpretation is in active rotation</dd>
  <dt>type</dt>
   <dd>Type of the interpretation (one of 'image', 'text', 'html', 'javascript')</dd>
  <dt>content_location</dt>
   <dd>URL (relative to the API host) where the interpretation's contents can be downloaded</dd>
  <dt>author_location</dt>
   <dd>URL (relative to the API host) where information about the author can be found</dd>
  <dt>decorated_location</dt>
   <dd>URL (relative to the API host) where the interpretation can be viewed</dd>
  <dt>short_url</dt>
   <dd>shortened (bit.ly) absolute URL to this interpretation</dd>
  <dt>comments</dt>
   <dd>number of comments associated with this interpretation</dd>
  <dt>image_height (iff type='image')</dt>
   <dd>height of the image, in pixels</dd>
  <dt>image_width (iff type='image')</dt>
   <dd>width of the image, in pixels</dd>
  <dt>javascript_hook (iff type='javascript')</dt>
   <dd>hook function to call to get the plugin object</dd>
 </dl>
 </div>

 <h3><a name="filter_parameters">Filter Parameters</a></h3>
 <div class="doc_block">
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
  <dt>type</dt>
   <dd>The interpretation type.</dd>
  <dt>offset_key_string</dt>
   <dd>A starting opaque key. Only interpretations whose key is &gt;= this value are considered. This is intended for use in pagination (see /list_pages and /list methods).</dd>
 </dl>
 </div>

 <h3 class="method_header"><a name="method_poot">/poot [GET]</a></h3>
 <div class="doc_block">
 <p>Given a set of <a href="#filter_parameters">filter parameters</a>, this returns <em>exactly one</em> <a href="#interpretation_object">interpretation object</a>, selected at random from the full set of matching interpretations.</p>
 </div>

 <h3 class="method_header"><a name="method_count">/count [GET]</a></h3>
 <div class="doc_block">
 <p>Given a set of <a href="#filter_parameters">filter parameters</a>, this returns a simple object containing the following:</p>
  <dl>
   <dt>count</dt>
    <dd>Number of interpretations matched by the specified filters.</dd>
  </dl>
 </div>

 <h3 class="method_header"><a name="method_list_pages">/list_pages [GET]</a></h3>
 <div class="doc_block">
 <p>Given a set of <a href="#filter_parameters">filter parameters</a> and, in addition:</p>
  <dl>
   <dt>items</dt>
    <dd>The number of interpretations per page.</dd>
  </dl> 
 <p>This returns a list of one or more objects, each of which contains the following:</p>
  <dl>
   <dt>page_number</dt>
    <dd>Page number, starting from 1.</dd>
   <dt>offset_key_string</dt>
    <dd>Offset to pass as in the <a href="#filter_parameters">filter parameters</a> to the <a href="#method_list">/list method</a> to obtain the interpretations for the specified page.</dd>
  </dl>
 </div>

 <h3 class="method_header"><a name="method_list">/list [GET]</a></h3>
 <div class="doc_block">
 <p>Given a set of <a href="#filter_parameters">filter parameters</a> and, in addition:</p>
  <dl>
   <dt>items</dt>
    <dd>The number of interpretations per page.</dd>
  </dl>
 <p>This returns a list of 1 to 'items' <a href="#interpretation_object">interpretation objects</a>.</p>
 <p>
 See the <a href="#method_list_pages">/list_pages method</a> above; these two methods need to be used together if you're trying to iterate over interpretations. Basically, you want to call /list_pages with the desired filters and 'items'. For each returned page, call /list with the page's offset_key_string (returned by /list_pages), as a filter in addition to the original arguments given to /list_pages.
 </p>
 </div>

 <h3 class="method_header"><a name="method_submit">/submit [POST]</a></h3>
 <div class="doc_block">
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
 </div>

 <h3 class="method_header"><a name="method_approve">/approve [POST]</a></h3>
 <div class="doc_block">
 <p>Make a submitted interpretation active. Requires the following arguments:</p>
 <dl>
  <dt>key_string</dt>
   <dd>Opaque unique identifier for this interpretation. You saved it after calling /submit, right?</dd>
  <dt>owner_baton</dt>
   <dd>You saved it after calling the <a href="#method_submit">/submit method</a>, right?</dd>
 </dl>
 <p>On success, returns the approved <a href="#interpretation_object">interpretation object</a>.</p>
 </div>
 
 <h3 class="method_header"><a name="method_disapprove">/disapprove [POST]</a></h3>
 <div class="doc_block">
 <p>Permanently delete a submitted interpretation. Requires the following arguments:</p>
 <dl>
  <dt>key_string</dt>
   <dd>Opaque unique identifier for this interpretation. You saved it after calling /submit, right?</dd>
  <dt>owner_baton</dt>
   <dd>You saved it after calling the <a href="#method_submit">/submit method</a>, right?</dd>
 </dl>
 <p>On success, returns the deleted <a href="#interpretation_object">interpretation object</a>.</p>
 </div>

 <h2>Comments</h2>
 <h3><a name="comment_object">Comment Objects</a></h3>
 <div class="doc_block">
 <p>Many of the comment API methods below return serialized comment data, which are objects
 consisting of:</p>
 <dl>
  <dt>author</dt>
   <dd>Author of the comment</dd>
  <dt>created_at</dt>
   <dd>Formatted date string (%a, %d %b %Y %H:%M:%S GMT) when this comment was created</dd>
  <dt>content</dt>
   <dd>The comment itself</dd>
 </dl>
 </div>

 <h3 class="method_header"><a name="method_comment_list">/comment_list [GET]</a></h3>
 <div class="doc_block">
 <p>Fetch all comments attached to a given interpretation. Requires the following argument:</p>
 <dl>
  <dt>interpretation_key_string</dt>
   <dd>The key_string from an <a href="#interpretation_object">interpretation object</a>.</dd>
  </dl>
  <p>On success, returns a list of <a href="#comment_object">comment objects</a>.</p>
  <dl>
   <dt>key_string</dt>
    <dd>Unique key identifying this comment</dd>
  </dl>
 </div>

 <h3 class="method_header"><a name="method_coment_submit">/comment_submit [POST]</a></h3>
 <div class="doc_block">
 <p>Create a new comment. Requires the following arguments:</p>
 <dl>
  <dt>interpretation_key_string</dt>
   <dd>The key_string from an <a href="#interpretation_object">interpretation object</a>. This will be the interpretation to which this comment is attached.</dd>
  <dt>author</dt>
   <dd>Author of the comment</dd>
  <dt>content</dt>
   <dd>The comment itself</dd>
  </dl>
  <p>On success, returns an object containing the following:</p>
  <dl>
   <dt>key_string</dt>
    <dd>Unique key identifying this comment</dd>
  </dl>
 </div>
 
 </div>
m4_include(bottom_links.m4)
</body>

</html>
