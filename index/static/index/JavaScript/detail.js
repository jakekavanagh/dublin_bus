// Declare Global variables
var my_lat, my_long, names;

// This function initializes the Map with a route according to the origin stop and destination stop input by the user
function initializeMapDetail() {

	userPosition = new google.maps.LatLng(my_lat, my_long);

	//creates object for Google Map API direction service
	var directionsServiceTransit = new google.maps.DirectionsService();
	var directionsDisplayTransit = new google.maps.DirectionsRenderer();

	//create GeoPoints for origin and destination stops
	origin = new google.maps.LatLng(origin_lat, origin_lon);
	destination = new google.maps.LatLng(destination_lat, destination_lon);

	var properties = {
		center: {lat: ((origin_lat + destination_lat) / 2), lng: ((origin_lon + destination_lon) / 2)},
		zoom: 13,
	};

	// create map object
	map = new google.maps.Map(document.getElementById("map"), properties);
	var marker_origin = new google.maps.Marker({
		position: origin,
		animation: google.maps.Animation.DROP,
		icon: {
			url: bus_image,
			scaledSize: new google.maps.Size(60, 90),
			origin: new google.maps.Point(0, 0),
			anchor: new google.maps.Point(30, 90)
		}
	});

    //set markers of origin and destination on map
	marker_origin.setMap(map);

	// initialize a info window and content for the window
	var contentString = '<div class="info-window">' + '<h4>' + origin_word + '</h4>' + '<div class="info-content">' + '<p>Origin Stop</p>' + '</div>' + '</div>';
	var infowindow = new google.maps.InfoWindow({
		content: contentString,
		maxWidth: 400,
	});

	infowindow.open(map, marker_origin);

	if (destination_num != origin_num) {
		var marker_dest = new google.maps.Marker({
			position: destination,
			animation: google.maps.Animation.DROP,
			icon: {
				url: bus_image,
				scaledSize: new google.maps.Size(60, 90),
				origin: new google.maps.Point(0, 0),
				anchor: new google.maps.Point(30, 90)
			}
		});

		marker_dest.setMap(map);

		var contentString2 = '<div class="info-window">' + '<h4>' + destination_word + '</h4>' +
            '<div class="info-content">' + '<p>Destination Stop</p>' + '</div>' + '</div>';
		var infowindow = new google.maps.InfoWindow({
			content: contentString2,
			maxWidth: 400,
		});

		infowindow.open(map, marker_dest);
		var markers = [marker_origin, marker_dest];
		var circle = {
			path: google.maps.SymbolPath.CIRCLE,
			fillColor: 'black',
			fillOpacity: .6,
			scale: 3.8,
			strokeColor: 'white',
			strokeWeight: 0
		};

		names = names.replace(/[\[\]']+/g, '')
		names = names.split(",");
		for (i = 0; i < names.length; i++) {
			names[i] = names[i].replace(/&#39;/g, "");
		}

        //create markers for all bus stops of journey
		var allMarkers = new Array();
		allMarkers.push(new google.maps.LatLng(origin_lat, origin_lon));
		for (i = 0; i < stops.length; i++) {
			allMarkers.push(new google.maps.LatLng(parseFloat(stops[i][0]), parseFloat(stops[i][1])));
			var marker = new google.maps.Marker({
				position: new google.maps.LatLng(parseFloat(stops[i][0]), parseFloat(stops[i][1])),
				map: map,
				title: names[i],
				icon: circle
			});
		}
		allMarkers.push(new google.maps.LatLng(destination_lat, destination_lon));
		marker.setMap(map); //set all markers on map

        // create a route for all stops by drawlines to connect them
		var route = new google.maps.Polyline({
			path: allMarkers,
			geodesic: false,
			strokeColor: 'rgb(25,25,112)',
			strokeOpacity: 0.7,
			strokeWeight: 3.5
		});
		route.setMap(map);
	} else {
		var markers = [marker_origin];
	}

	// Customise style of Google Map, removing extra function and default point of interests
	var styles = [
	    {"featureType": "landscape", "stylers": [{"saturation": -0}, {"lightness": 10}, {"visibility": "on"}]},
        {"featureType": "poi", "stylers": [{"visibility": "off"}]},
        {"featureType": "transit", "stylers": [{"visibility": "off"}]},
        {"featureType": "road.highway", "stylers": [{"saturation": 50}, {"visibility": "simplified"}]},
        {"featureType": "road.arterial", "stylers": [{"saturation": 30}, {"visibility": "simplified"}]},
        {"featureType": "road.local", "stylers": [{"saturation": 50}, {"lightness": 0}, {"visibility": "simplified"}]},
        {"featureType": "administrative", "stylers": [{"saturation": 20}, {"visibility": "on"}]},
        {"featureType": "water", "elementType": "geometry", "stylers": [{"lightness": -25}, {"saturation": -40}]},
        {"featureType": "water", "elementType": "labels", "stylers": [{"visibility": "on"}, {"saturation": 100}]},
    ];

	map.set('styles', styles);
	var bounds = new google.maps.LatLngBounds();
	for (var i = 0; i < markers.length; i++) {
		bounds.extend(markers[i].getPosition());
	}

	map.fitBounds(bounds);
	document.getElementById('mode_select').addEventListener('change', function() {
		if (document.getElementById('mode_select').value && document.getElementById('mode_select').value != "NULL") {
			Route(directionsServiceTransit, directionsDisplayTransit, origin, destination, document.getElementById('mode_select').value);
			directionsDisplayTransit.setMap(map);
		}
		if (document.getElementById('mode_select').value == "NULL") {
			if (directionsDisplayTransit != null) {
				directionsDisplayTransit.setMap(null);
				// directionsDisplayTransit = null;
				document.getElementById("Journey_duration").innerHTML = "";
				document.getElementById("Journey_distance").innerHTML = "";
			}
		}
	});

	// call 2 functions to generate event layer and twitter layer
	generateEventLayer();
	addTwitterAlert();
}