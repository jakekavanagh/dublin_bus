// Global Variables
var destination, origin, map, heatMap, directionsDisplayWalking, eventMarkers, map2, userPosition,
    location_icon, origin_lat, origin_lon, destination_lat, destination_lon, bus_image, origin_word, destination_word,
    infoExist = false, infowindow;

// This function executes if the detail HTML page is loaded
$(function() {
   $(window).on('load', function(){
    if($('body').is('.detail')){
        initializeMapDetail();
        addTwitterAlert();


    }
    if($('body').is('.find')){
        initializeMapFind();
    }
       });
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

    var location_image = location_icon;
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
//    currentPositionMarker.setMap(map2);

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
    // console.log("stuff",events_json);

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
function Route(directionsService, directionsDisplay, start, end, mode, m) {

    var check = false;

    if(mode=="WALKING2"){
        check = true;
        mode = "WALKING";
    };

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


            if (response.request.travelMode != "WALKING" || check) {
                mode = mode.slice(0, 1) + mode.slice(1, mode.length).toLowerCase();
                document.getElementById("Journey_duration").innerHTML = mode + " Time: " +"<b>" + duration + "</b>";
                document.getElementById("Journey_distance").innerHTML = mode + " Distance: " +"<b>" + distance + "</b>";
            }

            if (response.request.travelMode == "WALKING" && check != true) {
                // return {duration: duration, distance: distance};
                document.getElementById("walking_duration").innerHTML = "Walking Time: " +"<b>" + duration + "</b>";
                document.getElementById("walking_distance").innerHTML = "Walking distance: " +"<b>" + distance + "</b>";
            }
        } else {
        window.alert("Couldn't get directions:" + status);
        }
        if (m == map2){
            if (infoExist == true){
               infowindow.setMap(null);
            }
            infowindow = new google.maps.InfoWindow();
            infowindow.setContent(response.routes[0].legs[0].steps[0].distance.text + "<br>" + response.routes[0].legs[0].steps[0].duration.text + " ");
            infowindow.setPosition(response.routes[0].legs[0].steps[0].end_location);
            infowindow.open(map2);
            infoExist = true;
             }
    });
}
var m;


function toggleWalkingLayer(ma){
    if (ma == 'detail') {
        m = map;
    }
    else if (ma == 'find') {
        m = map2;
    }
   var walkingDivValue = document.getElementById("walkingLayer");
    if (document.getElementById("walkingLayer").value == "0") {
       walkingRoute(m);
       walkingDivValue.value = "1";
    }
    else if (document.getElementById("walkingLayer").value == "1" & m == map2){
        directionsDisplayWalking.setMap(null);
        walkingDivValue.value = "0";
        walkingRoute(m);
        walkingDivValue.value = "1";
    }
    else if (document.getElementById("walkingLayer").value == "1"){
        directionsDisplayWalking.setMap(null);
        walkingDivValue.value = "0";
        document.getElementById("walking_duration").innerHTML = "";
        document.getElementById("walking_distance").innerHTML = "";
    }
}


// Generates the Walking route on map, using User's GeoLocation to the origin stop
function walkingRoute(m) {
    // Customize the route display
    if (m == map2) {
        var custom = {
            preserveViewport: true,
            suppressMarkers: true,
            polylineOptions: {
                strokeColor: "green"
            }
        }
    }
    else {
        var custom = {
                suppressMarkers: true,
                polylineOptions: {
                    strokeColor: "green"
                }
            }
    }
    var directionsServiceWalking = new google.maps.DirectionsService();
    directionsDisplayWalking = new google.maps.DirectionsRenderer(custom);
//    var userPosition = new google.maps.LatLng(useCurrentPosition.lat, useCurrentPosition.lon);


    // Generate and displays the walking route to the origin stop
    Route(directionsServiceWalking, directionsDisplayWalking, userPosition, origin, "WALKING", m);

    directionsDisplayWalking.setMap(m);

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

$(document).ready(function() {
    $('.bus_info').click(function (e) {
        $(this).next().slideToggle();
        $(this).next().next().next().slideToggle();
    });
});
