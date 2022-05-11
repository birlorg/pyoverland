<!DOCTYPE html>
<html lang="en">
<head>

  <!-- Basic Page Needs
  –––––––––––––––––––––––––––––––––––––––––––––––––– -->
  <meta charset="utf-8">
  <title>pyOverlander - history</title>
  <meta name="description" content="history">
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
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.8.0/dist/leaflet.css"
   integrity="sha512-hoalWLoI8r4UszCkZ5kL8vayOGVae1oxXe/2A4AO6J9+580uKHDO3JdHb7NzwwzK5xr/Fs0W40kiNHxM9vyTtQ=="
   crossorigin=""/>
 <!-- Make sure you put this AFTER Leaflet's CSS -->
 <script src="https://unpkg.com/leaflet@1.8.0/dist/leaflet.js"
   integrity="sha512-BB3hKbKWOc9Ez/TAwyWxNXeoV9c1v6FIeYiBieIWkpLjauysF18NzgR1MBNBXf8/KABdlkX68nAhlwcDFLGPCQ=="
   crossorigin=""></script>
</head>
<body>

  <!-- Primary Page Layout
  –––––––––––––––––––––––––––––––––––––––––––––––––– -->
<div class="section top">
  <div class="container">
        <h4>My history</h4>
	</div>
<div class="section map">
<div id="map" style="width: 600px; height: 400px;"></div>
</div>

<!-- End Document
  –––––––––––––––––––––––––––––––––––––––––––––––––– -->
</body>
<footer>
<P>Turtle Image:  ID <a href="https://www.dreamstime.com/cheerful-turtle-icon-cartoon-illustration-cheerful-turtle-vector-icon-web-cheerful-turtle-icon-cartoon-style-image113535149#_">113535149</a> © Anatolii Riabokon | Dreamstime.com 
</footer>
<script>
% now = dat[1]
var map = L.map('map').setView([{{now['big_lat']}}, {{now['big_long']}}], 13);
L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox/streets-v11',
    tileSize: 512,
    zoomOffset: -1,
    accessToken: 'pk.eyJ1IjoicGVhY2V0YXJhIiwiYSI6ImNsMm9ha2p4cDAzdDczanEwNTlzdWRkZmgifQ.bDU2EzxY9xHOOesRYy7NQQ'
}).addTo(map);
var turtleIcon = L.icon({
    iconUrl: 'static/turtle-95.png',
    //shadowUrl: 'static/turtle-shadow95.png.',

    iconSize:     [38, 95], // size of the icon
    shadowSize:   [50, 64], // size of the shadow
    iconAnchor:   [22, 94], // point of the icon which will correspond to marker's location
    shadowAnchor: [4, 62],  // the same for the shadow
    popupAnchor:  [-3, -76] // point from which the popup should open relative to the iconAnchor
});
% for now in dat:
	var marker = L.marker([{{now['latitude']}}, {{now['longitude']}}], {icon: turtleIcon, alt: 'Me'}).addTo(map).bindPopup("{{now['human_time']}}");
% end
</script>
</html>
