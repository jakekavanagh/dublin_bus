var my_lat;
var my_long;

function initializeMapFind() {

    userPosition = new google.maps.LatLng(my_lat, my_long);
    origin = new google.maps.LatLng(lat_1, long_1);


    var routes = [routes_1, routes_2, routes_3, routes_4, routes_5]
    for (var i = 0; i < routes.length; i++) {
        routes[i] = routes[i].replace(/&#39;/g, "");
        routes[i] = routes[i].replace(/[\[\]']+/g,'');
        var x = routes[i].split(", ");
        var forButtons = x.slice(1,);
        var results = '<form action="detail/" method="post" autocomplete="off">'+ csrf;
        results += '<input name = "orig" type ="hidden" value="'+String(x[0])+'" />'
        results += '<input name = "current" type ="hidden" value="'+[my_lat, my_long]+'" />'
        for (var j = 0; j < forButtons.length; j++) {
            results += '<input name = "route" type="submit" value="'+forButtons[j]+'" />'
        }
        results += '</form>'
        document.getElementById(String(x[0])+"p").innerHTML = results;
    }

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
    var markers = [marker, marker2, marker3, marker4, marker5, user];
        var bounds = new google.maps.LatLngBounds();
        for (var i = 0; i < markers.length; i++) {
             bounds.extend(markers[i].getPosition());
        }
        map2.fitBounds(bounds);

//    marker.setMap(map2);
//    marker2.setMap(map2);
//    marker3.setMap(map2);
//    marker4.setMap(map2);
//    marker5.setMap(map2);
//    user.setMap(map2);

    user.addListener('mouseover', toggleBounce);

    markers = markers.slice(0,-1)

//    for (i = 0; i< markers.length; i++) {
//        alert(markers[i].title);
//        markers[i].addListener('click', function() {
//            document.getElementById(markers[i].title).innerHTML = "HELLO";
//        });
//    }

    marker.addListener('click', function() {
        for (i = 0; i< markers.length; i++) {
            origin = new google.maps.LatLng(lat_1, long_1);
            toggleWalkingLayer('find');
            if (markers[i] == marker){
                document.getElementById(markers[i].title).style.background = "silver";
            }
            else {
                document.getElementById(markers[i].title).style.background = "none";
            }
        }
    });

    marker2.addListener('click', function() {
        for (i = 0; i< markers.length; i++) {
            origin = new google.maps.LatLng(lat_2, long_2);
            toggleWalkingLayer('find');
            if (markers[i] == marker2){
                document.getElementById(markers[i].title).style.background = "silver";
            }
            else {
                document.getElementById(markers[i].title).style.background = "none";
            }
        }
    });

    marker3.addListener('click', function() {
        for (i = 0; i< markers.length; i++) {
            origin = new google.maps.LatLng(lat_3, long_3);
            toggleWalkingLayer('find');
            if (markers[i] == marker3){
                document.getElementById(markers[i].title).style.background = "silver";
            }
            else {
                document.getElementById(markers[i].title).style.background = "none";
            }
        }
    });

    marker4.addListener('click', function() {
        for (i = 0; i< markers.length; i++) {
            origin = new google.maps.LatLng(lat_4, long_4);
            toggleWalkingLayer('find');
            if (markers[i] == marker4){
                document.getElementById(markers[i].title).style.background = "silver";
            }
            else {
                document.getElementById(markers[i].title).style.background = "none";
            }
        }
    });

    marker5.addListener('click', function() {
        for (i = 0; i< markers.length; i++) {
            origin = new google.maps.LatLng(lat_5, long_5);
            toggleWalkingLayer('find');
            if (markers[i] == marker5){
                document.getElementById(markers[i].title).style.background = "silver";
            }
            else {
                document.getElementById(markers[i].title).style.background = "none";
            }
        }
    });

    function toggleBounce() {
        if (user.getAnimation() !== null) {
          user.setAnimation(null);
        } else {
          user.setAnimation(google.maps.Animation.BOUNCE);
        }
      }
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
    map2.set('styles', styles);

//    new google.maps2.event.trigger( marker, 'click' );

//document.getElementById()

}

function submit(x) {
    alert(x);
}
