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

