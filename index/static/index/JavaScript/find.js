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
}
