
var map3;
function initializeMapLuas() {
    console.log("In map")
    var properties = {
        center: new google.maps.LatLng(53.333834, -6.240236),
        zoom: 12,
    };

    map3 = new google.maps.Map(document.getElementById("map"), properties);

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
    map3.set('styles', styles);

    luas_markers();
    luasRealTime();
}


function luas_markers(){
    var luas_stops_json = JSON.parse(luas_stops);
    // console.log("stuff",luas_stops_json);

    for(var stop in luas_stops_json){
        var lat = luas_stops_json[stop]['fields']['stop_lat'];
        var lon = luas_stops_json[stop]['fields']['stop_lon'];

        var infoWindow = new google.maps.InfoWindow({
            content: '<div id="iw-container">' + luas_stops_json[stop]['fields']['stop_name'] +
                    '</div>',
            maxWidth: 350
        });

        if(luas_stops_json[stop]['fields']['line'] == "Green"){
            var stopMarker = new google.maps.Marker({
            position: new google.maps.LatLng(lat, lon),
            // animation: google.maps.Animation.DROP,
            info: infoWindow,
            icon: green_marker,
            });
        }

        if(luas_stops_json[stop]['fields']['line'] == "Red"){
            var stopMarker = new google.maps.Marker({
            position: new google.maps.LatLng(lat, lon),
            // animation: google.maps.Animation.DROP,
            info: infoWindow,
            icon: green_marker,
            });
        }

        // show on click
        google.maps.event.addListener(stopMarker, 'click', function () {
            this.info.open(map, this);
        });
        stopMarker.setMap(map3);
    }

}


function luasRealTime(){
    var luas_realtime_json = JSON.parse(luas_realtime);

    var html_red = "";
    var html_green ="";
    var stops_array_green = [];
    var stops_array_red = [];

    for(var a in luas_realtime_json){
        var line = luas_realtime_json[a]['fields']['line'];
        var stop_id = luas_realtime_json[a]['fields']['stop_id'];
        var duetime = luas_realtime_json[a]['fields']['duetime'];
        var direction = luas_realtime_json[a]['fields']['direction'];

        var content = "<li id='"+ stop_id +"'><div>" +
            "<h1 class='bus_info' id='"+ stop_id +"N'>"+ stop_id +"<i class='fa fa-chevron-circle-down' aria-hidden='true'></i></h1>" +
            "<h2 class='bus_info_expand' id='"+ stop_id +"I'></h2>" +
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



$(document).on("click", ".bus_info",function() {
    $(this).next().slideToggle();
    $(this).next().next().next().slideToggle();
});