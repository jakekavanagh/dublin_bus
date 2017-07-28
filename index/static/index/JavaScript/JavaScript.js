// Global Variables
var destination;
var origin;
var map, heatmap, map2;

// This function executes if the index HTML page is loaded
$(function() {
    if($('body').is('.index')){

    }
});

// This function executes if the detail HTML page is loaded
$(function() {
    if($('body').is('.detail')){
        initializeMapDetail();
        addTwitterAlert();
    }
    if($('body').is('.find')){
        initializeMapFind();
        }
});

// ___________________________________________ Functions _________________________________________________
// Add functions below here and call above in separate functions if needed in any of the HTML page

// Stores User's location to solve ASYNC problem
function useCurrentPosition(){
    this.lat = null;
    this.lon = null;

    // this.function1 = function() {
    //     console.log('useCoords:  '+ this.lat+' and '+ this.lon +' =) ');
    // }
}
// Create new object for User's GeoLocation
var useCurrentPosition = new useCurrentPosition();

if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(storeCurrentPosition)
}else {
      // Browser doesn't support Geolocation
      handleLocationError(false, infoWindow, map.getCenter());
}


// Updates the object to the User's GeoLocation
function storeCurrentPosition(position){

    var location_image = "../static/images/location_icon.png";
    var Lat = position.coords.latitude;
    var Lon = position.coords.longitude;

    useCurrentPosition.lat = Lat;
    useCurrentPosition.lon = Lon;

    var currentPositionMarker = new google.maps.Marker({
        position: new google.maps.LatLng({lat: Lat, lng: Lon}),
        animation: google.maps.Animation.DROP,
        icon: location_image
    });
    // map.setCenter(pos); // Centers the map to this point
    currentPositionMarker.setMap(map);

}


// This function initializes the Map with a route according to the origin stop and destination stop input by the user
function initializeMapDetail() {

    var directionsServiceTransit = new google.maps.DirectionsService();
    var directionsDisplayTransit = new google.maps.DirectionsRenderer();

    var ModeSelection = document.getElementById('mode_select').value;
    origin = new google.maps.LatLng(origin_lat, origin_lon);
    destination = new google.maps.LatLng(destination_lat, destination_lon);

    var properties = {
       center: {lat: 53.3498, lng: -6.2603},
       zoom: 12,
    };

    map = new google.maps.Map(document.getElementById("map"), properties);
    directionsDisplayTransit.setMap(map);

    Route(directionsServiceTransit, directionsDisplayTransit, origin, destination, ModeSelection);

    // Event listener for change of transport mode
    document.getElementById('mode_select').addEventListener('change', function() {
         Route(directionsServiceTransit, directionsDisplayTransit, origin, destination,
             document.getElementById('mode_select').value);
    });
}

function initializeMapFind() {

    var properties = {
       center: {lat: my_lat, lng: my_long},
       zoom: 16,
    };
    map2 = new google.maps.Map(document.getElementById("map"), properties);

    var marker = new google.maps.Marker({
        position: new google.maps.LatLng(lat_1, long_1),
        animation: google.maps.Animation.BOUNCE,
        map: map2,
        title: stop_1,
        icon: {
            url: 'https://cdn4.iconfinder.com/data/icons/maps-and-navigation-solid-icons-vol-1/72/44-512.png',
            scaledSize: new google.maps.Size(40, 50),
            origin: new google.maps.Point(0, 0),
            anchor: new google.maps.Point(20, 50)
            }
      });
     var marker2 = new google.maps.Marker({
        position: new google.maps.LatLng(lat_2, long_2),
        animation: google.maps.Animation.BOUNCE,
        map: map2,
        title: stop_2,
        icon: {
            url: 'https://cdn4.iconfinder.com/data/icons/maps-and-navigation-solid-icons-vol-1/72/44-512.png',
            scaledSize: new google.maps.Size(40, 50),
            origin: new google.maps.Point(0, 0),
            anchor: new google.maps.Point(20, 50)
            }
     });
     var marker3 = new google.maps.Marker({
        position: new google.maps.LatLng(lat_3, long_3),
        animation: google.maps.Animation.BOUNCE,
        map: map2,
        title: stop_3,
        icon: {
            url: 'https://cdn4.iconfinder.com/data/icons/maps-and-navigation-solid-icons-vol-1/72/44-512.png',
            scaledSize: new google.maps.Size(40, 50),
            origin: new google.maps.Point(0, 0),
            anchor: new google.maps.Point(20, 50)
            }
    });
    var marker4 = new google.maps.Marker({
        position: new google.maps.LatLng(lat_4, long_4),
        animation: google.maps.Animation.BOUNCE,
        map: map2,
        title: stop_4,
        icon: {
            url: 'https://cdn4.iconfinder.com/data/icons/maps-and-navigation-solid-icons-vol-1/72/44-512.png',
            scaledSize: new google.maps.Size(40, 50),
            origin: new google.maps.Point(0, 0),
            anchor: new google.maps.Point(20, 50)
            }
    });
    var marker5 = new google.maps.Marker({
        position: new google.maps.LatLng(lat_5, long_5),
        animation: google.maps.Animation.BOUNCE,
        map: map2,
        title: stop_5,
        icon: {
            url: 'https://cdn4.iconfinder.com/data/icons/maps-and-navigation-solid-icons-vol-1/72/44-512.png',
            scaledSize: new google.maps.Size(40, 50),
            origin: new google.maps.Point(0, 0),
            anchor: new google.maps.Point(20, 50)
            }
    });

var user = new google.maps.Marker({
        position: new google.maps.LatLng(my_lat, my_long),
        animation: google.maps.Animation.DROP,
        map: map2,
        icon: {
            url: '../static/images/location_icon.png',
            scaledSize: new google.maps.Size(40, 50),
            origin: new google.maps.Point(0, 0),
            anchor: new google.maps.Point(20, 50)
            }

    });

//    marker.setMap(map2);
//    marker2.setMap(map2);
//    marker3.setMap(map2);
//    marker4.setMap(map2);
//    marker5.setMap(map2);
//    user.setMap(map2);
    user.addListener('mouseover', toggleBounce);

function toggleBounce() {
        if (user.getAnimation() !== null) {
          user.setAnimation(null);
        } else {
          user.setAnimation(google.maps.Animation.BOUNCE);
        }
      }
}


// generates a route on map, input variables include: origin, destination and travel mode.
// available modes: "DRIVING", "WALKING", "BICYCLING","TRANSIT"
function Route(directionsService, directionsDisplay, start, end, mode) {

    var requests = {
        origin: start,
        destination: end,
        travelMode: google.maps.TravelMode[mode]
    };

    directionsService.route(requests, function(response, status) {
        if (status == "OK") {
            directionsDisplay.setDirections(response);

            var duration = response.routes[0].legs[0].duration.text;
            var distance = response.routes[0].legs[0].distance.text;

            if (response.request.travelMode == "WALKING") {
                return {duration: duration, distance: distance};

            }
        } else {
        window.alert("Couldn't get directions:" + status);
        }
    });
}



// Generates the Walking route on map, using User's GeoLocation to the origin stop
function walkingRoute() {
    // Customize the route display
    var custom = {
        suppressMarkers: true,
        polylineOptions: {
            strokeColor: "green"
        }
    }
    var directionsServiceWalking = new google.maps.DirectionsService();
    var directionsDisplayWalking = new google.maps.DirectionsRenderer(custom);
    var userPosition = new google.maps.LatLng(useCurrentPosition.lat, useCurrentPosition.lon);


    // Generate and displays the walking route to the origin stop
    // console.log("Running route in walkingRoute")
    Route(directionsServiceWalking, directionsDisplayWalking, userPosition, origin, "WALKING");

    directionsDisplayWalking.setMap(map);
    // generateEventLayer();

}


// Generate alert icons on the map to show road incidents within 2 hours
function addTwitterAlert(){
   var tweety = JSON.parse(tweet);
   var delayImage = "../static/images/delay_icon.png";
   var infoWindow = new google.maps.InfoWindow();
   for(var i in tweety){
       var marker = new google.maps.Marker({
           position: {lat: tweety[i][2][0], lng: tweety[i][2][1]},
           map: map,
           icon: delayImage
       });
       google.maps.event.addListener(marker, 'click', (function (marker, i) {
           return function () {
           infoWindow.setContent(tweety[i][0]);
           infoWindow.open(map, marker);
           }
       })(marker, i));
   }
}

