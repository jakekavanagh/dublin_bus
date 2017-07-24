// Global Variables
var destination;
var origin;
var map, heatmap;

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
            console.log("does it work?", response)
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
    console.log("Running route in walkingRoute")
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


// function generateEventLayer(){
//     console.log("Clicked")
//     heatmap = new google.maps.visualization.HeatmapLayer({
//       data: eventLocations(),
//       map: map
//     });
//     // eventLocations();
//     // console.log("show me", events)
// }

// function eventLocations(){
//     console.log("data for events", events[0])
// }

// __________________________________ Code Back-up ( Code currently not in use) ________________________________
// Expand for the function


// function used for cookies
    /*
     var user_name;
     var expires = new Date();
     var length = document.cookie.length -1;
     var message = document.cookie.substring(5, length)
     document.write("<h5><center> Welcome Back, " + message + "!</center></h5>")
     function cookierun(){
     user_name = document.getElementById("name").value;
     expires.setFullYear(expires.getFullYear()+1);
     document.cookie = escape("name") + "=" + escape(user_name) + "; expires = " + expires.toUTCString();
     window.alert(document.cookie);
     }
     */

// function for google map api distance matrix
    /*
    function distanceMatrix(){

        var DistanceMatrix = new google.maps.DistanceMatrixService();
        var origin = new google.maps.LatLng(Lat, Lon);
        destination = new google.maps.LatLng(origin_lat, origin_lon);

        DistanceMatrix.getDistanceMatrix(
          {
            origins: [origin],
            destinations: [destination],
            travelMode: 'WALKING',
            unitSystem: google.maps.UnitSystem.METRIC

          }, function WalkingRoute_response(response, status){
              console.log("In a function for walking baby")
                if (status !== 'OK') {
                    alert('Error! ', status);
                } else {
                    var walking_distance = response['rows'][0]['elements'][0]['distance']['text'];
                    var walking_duration = response['rows'][0]['elements'][0]['duration']['text'];
                }
            }
        )

    }
    */

// Function to resize the Page
    /*
    $(document).ready(function(){
        if($(window).width() <= 1200) {
            window.location = "/indexmobile.html";
        }
    });
    $(window).resize(function(){location.reload();});
    */

// Function that executes function on load and function to generate today's day>
    /*
    google.maps.event.addDomListener(window, 'load', initialize);
    var td = new Date().getDay();
    td = (td == 0) ? 7 : td;
    $('select[id=day]').find('option').eq( td ).prop('selected', true)
        .end().change();
    });
    */

// Function to Generate bus stop markers
    /*
   $(function() {
       var xmlhttp = new XMLHttpRequest();
       var url = 'karl.json';
       var karldata;
       var map;
       xmlhttp.onreadystatechange = function() {
           if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
               karldata = JSON.parse(xmlhttp.responseText);
               addGPSmarker();
           }
       };
       xmlhttp.open("GET", url, true);
       xmlhttp.send();
       map = new google.maps.Map(document.getElementById('map'), {
           center: {lat: 53.3498, lng: -6.2603},
           zoom: 8
       });
       function addGPSmarker() {
           for(var i in karldata){
               var marker = new google.maps.Marker({
                   position: {lat: karldata[i]['Lat'], lng: karldata[i]['Lon']},
                   map: map,
                   label: i
               });
           }
       };
       */

// Function to check to geolocation availability
    /*
    function handleLocationError(browserHasGeolocation, infoWindow, pos) {
       infoWindow.setPosition(pos);
       infoWindow.setContent(browserHasGeolocation ?
           'Error: The Geolocation service failed.' :
           'Error: Your browser doesn\'t support geolocation.');
       infoWindow.open(map);
    }
    */

// Function to find geolocation generates a info window to say you are here
    /*
      function geolocation {
          // Try HTML5 geolocation.
          if (navigator.geolocation) {
              navigator.geolocation.getCurrentPosition(function (position) {
                  var pos = {
                      lat: position.coords.latitude,
                      lng: position.coords.longitude
                  };
                  infoWindow.setPosition(pos);
                  infoWindow.setContent('You are here');
                  infoWindow.open(map);
                  map.setCenter(pos);
              }, function () {
                  handleLocationError(true, infoWindow, map.getCenter());
              });
          } else {
              // Browser doesn't support Geolocation
              handleLocationError(false, infoWindow, map.getCenter());
          }
      }
    */

