// Global Variables
var destination, origin, map, heatMap, directionsDisplayWalking, eventMarkers;


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
    generateEventLayer()
}


function toggleEventLayer(){

     if (heatMap.getMap() != null) {
        heatMap.setMap(null);
        for (var i = 0; i < eventMarkers.length; i++) {
            eventMarkers[i].setVisible(false);
        }
    } else {
        heatMap.setMap(map);
        for (var i = 0; i < eventMarkers.length; i++) {
            eventMarkers[i].setVisible(true);
        }
    }
}


function generateEventLayer(){

    heatMap = new google.maps.visualization.HeatmapLayer({
        dissipating: true,
        data: generateEventPoints(),
        map: map,
        radius: 35,
    });
}


function generateEventPoints(){

    var events_json = JSON.parse(events);

    var points = []
    eventMarkers = []
    for(var e in events_json){
        var infoWindow = new google.maps.InfoWindow({
            content: '<div id="iw-container">' +
                        '<div class="iw-title"><h4>'+ events_json[e]["fields"]["venue_name"] +'</h4> </div>' +
                            '<div class="iw-content"><h5>'+ events_json[e]["fields"]["title"] +'</h5></div>' +
                                '<p><h6>Address:'+ events_json[e]["fields"]["venue_address"] +'</h6></p>'+
                        '<div class="iw-bottom-gradient"></div>' +
                    '</div>',
            maxWidth: 350
        });

        var event_lat = events_json[e]['fields']['latitude'];
        var event_lon = events_json[e]['fields']['longitude'];
        var geoPoint = new google.maps.LatLng(event_lat, event_lon);
        points.push(geoPoint);

        // var icon_hover = "../static/images/search.png";
        var invis_icon = "../static/images/invisible_marker.png";

        var eMarker = new google.maps.Marker({
            position: new google.maps.LatLng(event_lat, event_lon),
            animation: google.maps.Animation.DROP,
            info: infoWindow,
            icon: invis_icon
            // icon: "https://maps.gstatic.com/intl/en_us/mapfiles/markers2/measle_blue.png"
        });

        // show on click
        google.maps.event.addListener(eMarker, 'click', function () {
            this.info.open(map, this);
        });

        // // show on hover
        // google.maps.event.addListener(eMarker, 'mouseover', function () {
        //     this.icon.setIcon(icon_hover, this);
        // //     this.info.open(map, this);
        // });
        // google.maps.event.addListener(eMarker, 'mouseout', function () {
        //     this.icon.setIcon(invis_icon);
        //     // this.info.close();
        // });

        eventMarkers.push(eMarker);
        eMarker.setMap(map);
    }
    return points
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
                // return {duration: duration, distance: distance};
            document.getElementById("walking_duration").innerHTML = duration;
            document.getElementById("walking_distance").innerHTML = distance;

            }
        } else {
        window.alert("Couldn't get directions:" + status);
        }
    });
}

function toggleWalkingLayer(){
   var walkingDivValue = document.getElementById("walkingLayer");
    if (document.getElementById("walkingLayer").value == "0") {
       walkingRoute();
       walkingDivValue.value = "1";
    } else if (document.getElementById("walkingLayer").value == "1"){
    directionsDisplayWalking.setMap(null);
    walkingDivValue.value = "0";
    document.getElementById("walking_duration").innerHTML = "";
    document.getElementById("walking_distance").innerHTML = "";

    }

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
    directionsDisplayWalking = new google.maps.DirectionsRenderer(custom);
    var userPosition = new google.maps.LatLng(useCurrentPosition.lat, useCurrentPosition.lon);


    // Generate and displays the walking route to the origin stop
    Route(directionsServiceWalking, directionsDisplayWalking, userPosition, origin, "WALKING");

    directionsDisplayWalking.setMap(map);

}


// Generate alert icons on the map to show road incidents within 2 hours
function addTwitterAlert(){
   var tweety = JSON.parse(tweet);
   // console.log(tweety)
    var delayImage = "../static/images/delay_icon.png";
    var infoWindow = new google.maps.InfoWindow();

    for(var t in tweety){
       console.log(tweety[t])
       var marker = new google.maps.Marker({
           position: {lat: tweety[t]['fields']['latitude'],
                      lng: tweety[t]['fields']['longitude']},
           map: map,
           icon: delayImage
       });
       google.maps.event.addListener(marker, 'click', (function (marker, i) {
           return function () {
           infoWindow.setContent(tweety[t]['fields']['tweet']);
           infoWindow.open(map, marker);
           }
       })(marker, t));
   }
}



// function eventMarkersToggle

// function generateEventMarker(){

    // var event_marker = new google.maps.Marker({
    //     position: new google.maps.LatLng(event_lat, event_lon),
    //     info: infowindow
    // });
    // event_marker.setMap(heatMap);
//
//         event_marker.addListener('mouseover', function() {
//         infowindow.open(map, this);
//     });
//
//     // assuming you also want to hide the infowindow when user mouses-out
//     event_marker.addListener('mouseout', function() {
//         infowindow.close();
//     });
// }
