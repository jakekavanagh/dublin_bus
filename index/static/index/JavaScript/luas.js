// declare map as global variable
var map3;

// Initializes the map for the luas.html page
function initializeMapLuas(){

    var properties = {
        center: new google.maps.LatLng(53.333834, -6.240236),
        zoom: 12,
    };

    map3 = new google.maps.Map(document.getElementById("map"), properties);

    //Customize the google map object for more simplistic look
    var styles = [{"featureType": "landscape", "stylers": [{"saturation": -0}, {"lightness": 10}, {"visibility": "on"}]},
    {"featureType": "poi", "stylers": [{"visibility": "off"}]},
    {"featureType": "transit", "stylers": [{"visibility": "off"}]},
    {"featureType": "road.highway", "stylers": [{"saturation": 50}, {"visibility": "simplified"}]},
    {"featureType": "road.arterial", "stylers": [{"saturation": 30},  {"visibility": "simplified"}]},
    {"featureType": "road.local", "stylers": [{"saturation": 50}, {"lightness": 0}, {"visibility": "simplified"}]},
    {"featureType": "administrative", "stylers": [{"saturation": 20}, {"visibility": "on"}]},
    {"featureType": "water", "elementType": "geometry", "stylers": [ {"lightness": -25}, , {"saturation": -40}]},
    {"featureType": "water", "elementType": "labels", "stylers": [{"visibility": "on"}, {"saturation": 100}]},
    ];
    map3.set('styles', styles); //The the style on the map object

    // Calls functions to generate markers on map and another to display arrival times
    luas_markers();
    luasRealTime();
}

// Using parsed in json data, generate through iteration markers for all stops to show on the map object
function luas_markers(){
    var luas_stops_json = JSON.parse(luas_stops);

    for(var stop in luas_stops_json){
        var lat = luas_stops_json[stop]['fields']['stop_lat'];
        var lon = luas_stops_json[stop]['fields']['stop_lon'];

        var infoWindow = new google.maps.InfoWindow({
            content: '<div id="iw-container">' + luas_stops_json[stop]['fields']['stop_name'] +
                    '</div>',
            maxWidth: 350
        });

        // generates a new marker for GreenLine timetable if the condition is satisfied
        if(luas_stops_json[stop]['fields']['line'] == "Green"){
            var stopMarker = new google.maps.Marker({
            position: new google.maps.LatLng(lat, lon),
            // animation: google.maps.Animation.DROP,
            info: infoWindow,
            icon: green_marker,
            });
        }

        // generates a new marker for RedLine timetable if the condition is satisfied
        if(luas_stops_json[stop]['fields']['line'] == "Red"){
            var stopMarker = new google.maps.Marker({
            position: new google.maps.LatLng(lat, lon),
            // animation: google.maps.Animation.DROP,
            info: infoWindow,
            icon: red_marker,
            });
        }

        // Display info window content on click of marker
        google.maps.event.addListener(stopMarker, 'click', function () {
            this.info.open(map, this);
        });
        stopMarker.setMap(map3);
    }

}

// Using parsed in JSON data to display arrival times
function luasRealTime(){
    var luas_realtime_json = JSON.parse(luas_realtime);

    // Declare variables
    var html_red = "";
    var html_green ="";
    var stops_array_green = [];
    var stops_array_red = [];

    // Iterator to generate arrival time
    for(var a in luas_realtime_json){
        var line = luas_realtime_json[a]['fields']['line'];
        var stop_id = luas_realtime_json[a]['fields']['stop_id'];
        var duetime = luas_realtime_json[a]['fields']['duetime'];
        var direction = luas_realtime_json[a]['fields']['direction'];

        var content = "<li id='"+ stop_id +"'><div>" +
            "<h5 style='font-size: 1.1em;' class='bus_info' id='"+ stop_id +"N'>"+ stop_id +"<i class='fa fa-chevron-circle-down' aria-hidden='true'></i></h5>" +
            "<h6 class='bus_info_expand' id='"+ stop_id +"I'></h6>" +
            "</div></li>"

        if(stops_array_green.includes(stop_id) != true && line == "Green"){
            stops_array_green.push(stop_id)
            html_green += content;
        }
        if(stops_array_red.includes(stop_id) != true && line == "Red"){
            stops_array_red.push(stop_id)
            html_red += content;
        }

    }

    // Display the newly generated information
    document.getElementById('timeline').innerHTML = html_green;
    document.getElementById('timeline2').innerHTML = html_red;

    var luas_stops_json = JSON.parse(luas_stops);
    for (var name in luas_stops_json){
        var stop_name = luas_stops_json[name]['fields']['stop_name'];
        document.getElementById(luas_stops_json[name]['fields']['stop_id']+"N").innerHTML = stop_name;
    }

    for(var a in luas_realtime_json) {
        var line = luas_realtime_json[a]['fields']['line'];
        var stop_id = luas_realtime_json[a]['fields']['stop_id'];
        var duetime = luas_realtime_json[a]['fields']['duetime'];
        var direction = luas_realtime_json[a]['fields']['direction'];

        var content_duetimes = "<p>"+ direction +"  Due:"+ duetime +"</p>"
        var info = document.getElementById(stop_id+"I");
        info.insertAdjacentHTML('beforeend', content_duetimes);
    }
}


// function for controlling toggle on the TimeLine
$(document).on("click", ".bus_info",function() {
    $(this).next().slideToggle();
    $(this).next().next().next().slideToggle();
});