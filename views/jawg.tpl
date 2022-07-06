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
  <link rel="stylesheet" href="static/Skeleton-2.0.4/css/skeleton.css">
  <link rel="stylesheet" href="static/Skeleton-2.0.4/css/normalize.css">
  –––––––––––––––––––––––––––––––––––––––––––––––––– -->

  <!-- Favicon
  –––––––––––––––––––––––––––––––––––––––––––––––––– -->
  <link rel="icon" type="image/png" href="static/Skeleton-2.0.4/images/favicon.png">
  
  <!-- Map
  –––––––––––––––––––––––––––––––––––––––––––––––––– -->

  <link rel="stylesheet" href="http://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.3/leaflet.css"/>
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.4.0/css/font-awesome.min.css">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet.markercluster/0.4.0/MarkerCluster.css"/>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet.markercluster/0.4.0/MarkerCluster.Default.css"/>
  <link rel="stylesheet" href="static/jawg/style/samples.css"/>
  <link rel="stylesheet" href="static/jawg/widgets/search/search-widget.css"/>
  <link rel="stylesheet" href="static/jawg/widgets/filters/filters-widget.css"/>
  <link rel="stylesheet" href="static/jawg/widgets/markers/markers-widget.css"/>
  <link rel="stylesheet" href="static/jawg/widgets/layers/layers-widget.css"/>
</head>
<body>

  <!-- Primary Page Layout
  –––––––––––––––––––––––––––––––––––––––––––––––––– -->
<div class="section top">
  <div class="container">
        <h4>Where am I?</h4>
        <p>My last recorded location was on <time datetime={{now['timestamp']}}>{{now['human_time']}}</time> , which was about {{now['time_ago']}} at these coordinates: ({{now['latitude']}}, {{now['longitude']}}).</P>
	You can map me on openstreetmaps <a href="{{now['openstreetmap_url']}}">here</A>
	</div>
&nbsp;
&nbsp;
&nbsp;
&nbsp;
&nbsp;
&nbsp;
&nbsp;
&nbsp;
<div class="section map" >
  <div class="container">
<div class="map-position" >
  <div id="widget"></div>
</div>
  </div>
</div>

<!-- End Document
  –––––––––––––––––––––––––––––––––––––––––––––––––– -->
</body>
<script src="http://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.3/leaflet.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet.markercluster/0.4.0/leaflet.markercluster.js"></script>
<script src="static/jawg/widgets/mapSample.js"></script>
<script src="static/jawg/widgets/search/search-widget.js"></script>
<script src="static/jawg/widgets/filters/filters-widget.js"></script>
<script src="static/jawg/widgets/markers/markers-widget.js"></script>
<script src="static/jawg/widgets/layers/layers-widget.js"></script>
<script>
  var mapConf = {
    "tileServer": "http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
    "poiServer": "",
    "mapBounds": [[50, 180], [30, -180]],
    "widgetConf": {
      "panelPosition": "left",
      "osmSearch": true,
      "clickMarker": true
    },
    "points" : [[{{now['big_lat']}}, {{now['big_long']}}]],
    "minZoom": 3,
    "maxZoom": 18,
    "initialZoom": 6,
    "initialLocation": [{{now['big_lat']}}, {{now['big_long']}}],
    "fitBounds": null,
    "clusterMaxLevel": 19
  };
  MapManager.callMap('widget', mapConf, [
    "search-widget",
    "markers-widget"
  ]);
</script>
</html>
