<!DOCTYPE html>
<html lang="en">
<head>

  <!-- Basic Page Needs
  –––––––––––––––––––––––––––––––––––––––––––––––––– -->
  <meta charset="utf-8">
  <title>pyOverlander - now</title>
  <meta name="description" content="Where am I now?">
  <meta name="author" content="zie@zie.one">

  <!-- Mobile Specific Metas
  –––––––––––––––––––––––––––––––––––––––––––––––––– -->
  <meta name="viewport" content="width=device-width, initial-scale=1">

  <!-- FONT
  <link href="//fonts.googleapis.com/css?family=Raleway:400,300,600" rel="stylesheet" type="text/css">
  –––––––––––––––––––––––––––––––––––––––––––––––––– -->

  <!-- CSS
  –––––––––––––––––––––––––––––––––––––––––––––––––– -->
  <link rel="stylesheet" href="static/Skeleton-2.0.4/css/normalize.css">
  <link rel="stylesheet" href="static/Skeleton-2.0.4/css/skeleton.css">

  <!-- Favicon
  –––––––––––––––––––––––––––––––––––––––––––––––––– -->
  <link rel="icon" type="image/png" href="static/Skeleton-2.0.4/images/favicon.png">

</head>
<body>

  <!-- Primary Page Layout
  –––––––––––––––––––––––––––––––––––––––––––––––––– -->
  <div class="container">
        <h4>Where am I?</h4>
        <p>My last recorded location was on <time datetime={{now['timestamp']}}>{{now['human_time']}}</time> , which was about {{now['time_ago']}} at these coordinates: ({{now['latitude']}}, {{now['longitude']}}).</P>
	You can map me on openstreetmaps <a href="{{now['openstreetmap_url']}}">here</A>
  </div>

<!-- End Document
  –––––––––––––––––––––––––––––––––––––––––––––––––– -->
</body>
</html>
