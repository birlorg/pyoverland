<!DOCTYPE html>
<html lang="en">
<head>

  <!-- Basic Page Needs
  –––––––––––––––––––––––––––––––––––––––––––––––––– -->
  <meta charset="utf-8">
  <title>pyOverlander - now</title>
  <meta name="description" content="Where am I now?">
  <meta name="author" content="zie@turtle.st">

  <!-- Mobile Specific Metas
  –––––––––––––––––––––––––––––––––––––––––––––––––– -->
  <meta name="viewport" content="width=device-width, initial-scale=1.0">

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
<link rel="stylesheet" href="static/leaflet.css"
   integrity="sha512-hoalWLoI8r4UszCkZ5kL8vayOGVae1oxXe/2A4AO6J9+580uKHDO3JdHb7NzwwzK5xr/Fs0W40kiNHxM9vyTtQ=="
   />
 <!-- Make sure you put this AFTER Leaflet's CSS -->
 <script src="static/leaflet.js"
   integrity="sha512-BB3hKbKWOc9Ez/TAwyWxNXeoV9c1v6FIeYiBieIWkpLjauysF18NzgR1MBNBXf8/KABdlkX68nAhlwcDFLGPCQ=="
   ></script>
<link rel="stylesheet" href="static/css/water.css"
   integrity="sha384-eHoWBq4xGyEfS3rmZe6gvzlNS/nNJhiPPbKCJN1cQHJukU+q6ji3My2fJGYd1EBo"
   />
</head>
<body>

  <!-- Primary Page Layout
  –––––––––––––––––––––––––––––––––––––––––––––––––– -->
<div class="section top">
  <div class="container">
        <h4>Where am I?</h4>
        <p>My last recorded location was on <time datetime={{now['timestamp']}}>{{now['human_time']}}</time> 
, which was about {{now['time_ago']}} at these coordinates: ({{now['latitude']}}, {{now['longitude']}}).</P>
	
<P>Different mapping platforms:
<UL>
<LI><a href="{{now['apple_maps_url']}}">Apple Maps</A></LI>
<LI><a href="{{now['openstreetmap_url']}}">OpenStreetMap</A></LI>
</UL>
<h3>My Weather:</h3>
% if now['weather']:
	% if now['weather'].alerts: 
	<h4>Alerts:</h4>
		<UL>
		% for alert in now['weather'].alerts:
		<LI>{{alert.headline}}</LI>
		</UL>
		% end
	% end
<table id="weather" border=1>
	% for forecast in now['weather'].properties.periods:
	<tr><td>{{forecast.name}}</td><td>{{forecast.temperature}}{{forecast.temperatureUnit}}</td><td>{{forecast.detailedForecast}}</td></tr>
<!--	<P>now['weather']['forecast']['detailedForecast']</P> -->
	% end
	</table>
% else:
<P>Unforunately api.weather.gov is being mean at the moment, refresh to try again.</P>
% end
</div>
<h3>My Map:</h3>
<div class="section map">
<div id="map" style="width: 800px; height: 600px;"></div>
</div>

<!-- End Document
  –––––––––––––––––––––––––––––––––––––––––––––––––– -->
</body>
<footer>
<P>Turtle Image:  ID <a href="https://www.dreamstime.com/cheerful-turtle-icon-cartoon-illustration-cheerful-turtle-vector-icon-web-cheerful-turtle-icon-cartoon-style-image113535149#_">113535149</a> © Anatolii Riabokon | Dreamstime.com 
</footer>
<script>
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
var marker = L.marker([{{now['latitude']}}, {{now['longitude']}}], {icon: turtleIcon, alt: 'Me'}).addTo(map).bindPopup("Turtle's location");
</script>
</html>
