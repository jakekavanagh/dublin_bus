function populate(route, dict, locations) {
     route = route;
     var zero = [dict[route]['0']];
     var one = [dict[route]['1']];
     if (zero == ''){
        alert("no zero");
        all_stops = one;
     } else if (one == ''){
        alert("no one");
        all_stops = zero;
     } else {
        all_stops = zero.concat(one);
     }
     var array = JSON.parse("["+all_stops+"]");
     <!--array.sort(function(a, b){return a-b});-->
     var dropdown = document.getElementById("origin");
     while (dropdown.options.length > 0) {
        dropdown.remove(0);
    }
     var option = document.createElement("option");
     option.text = "Select an Origin Stop";
     dropdown.add(option);
     alert(array);
     for (var i = 0; i < array.length; ++i) {
          var option = document.createElement("option");
          option.text = locations[array[i]]['name'] +' - '+ array[i];
          option.value = array[i];
          dropdown.add(option);
     }

     var desti = document.getElementById("destination");
     while (desti.options.length > 0) {
        desti.remove(0);
     }
     var option = document.createElement("option");
     option.text = "Select Origin Stop First";
     desti.add(option);

}


function populateDestination(start, dict, locations) {
    var route = document.getElementById("RouteNumbers").value;
    var subset;
    if ($.inArray(start, dict[route]['0']) != -1){
        subset = dict[route]['0'].slice($.inArray(start, dict[route]['0'])+1, );
    }
    if ($.inArray(start, dict[route]['1']) != -1){
        var temp = dict[route]['1'].slice($.inArray(start, dict[route]['1'])+1, );
        if(typeof subset == 'undefined'){
            subset = temp;
        }
        else {
            subset = subset.concat(temp);
        }
    }

     var dropdown = document.getElementById("destination");
     while (dropdown.options.length > 0) {
        dropdown.remove(0);
     }

    var originValue = document.getElementById("origin").value;
     var option = document.createElement("option");
     option.text = "Select a Destination Stop";
     option.value = originValue;
     dropdown.add(option);

     destination.options[destination.options.selectedIndex].setAttribute("selected", "selected");

     for (var i = 0; i < subset.length; ++i) {
          var option = document.createElement("option");
          option.text = locations[subset[i]]['name'] + ' - '+ subset[i];
          option.value = subset[i];
          dropdown.add(option);
     }

}

function saveValues()
{

    var routevalue = document.getElementById("RouteNumbers");
    var originvalue = document.getElementById("origin");
    var destinationvalue = document.getElementById("destination");
    var timevalue = document.getElementById("time");
    var dayvalue = document.getElementById("day");


    localStorage._route = routevalue.value;
    localStorage._origin = originvalue.value;
    localStorage._destination = destinationvalue.value;
    localStorage._time = timevalue.value;
    localStorage._day = dayvalue.value;


//    localStorage._route = routevalue.options[routevalue.selectedIndex].text;
//    localStorage._origin = originvalue.options[originvalue.selectedIndex].text;
//    localStorage._destination = destinationvalue.options[destinationvalue.selectedIndex].text;
//    localStorage._time = document.timevalue.options[timevalue.selectedIndex].text;
//    localStorage._day = document.dayvalue.options[dayvalue.selectedIndex].text;
}
function loadValues()
{
    var route = localStorage._route;
    var origin = localStorage._origin;
    var destination = localStorage._destination;
    var time = localStorage._time;
    var day = localStorage._day;

    var x = document.getElementById('MyPreference');
    if(route == null){
        return;
    }else{
    if (x.style.display === 'none') {
        x.style.display = 'block';
    } else {
        x.style.display = 'none';
    }

//    var desti;
//    var title_string;
//    if (destination == origin){
//        title_string = "";
//        desti = origin;
//    }
//    else {
        title_string =  ' to ' + destination;
//        desti = destination;
//    }

    var title = 'You\'ve been here before! Would you like to search route '+route+' from ' + origin + title_string +' again?';

    var result = '<input name = "orig" type ="hidden" value="'+origin+'"+/>' +
    '<input name = "dest" type ="hidden" value="'+destination+'"+/>' +
    '<input name = "route" type="hidden" value="'+route+'" />';

    document.getElementById('title').innerHTML = title;
    document.getElementById('fillForm').innerHTML = result;
//    document.getElementById("myroute").textContent=route;
//    document.getElementById("myorigin").textContent=origin;
//    document.getElementById("mydest").textContent=destination;
//    document.getElementById("mytime").textContent=time;
//    document.getElementById("myday").textContent=day;
}}
function No_Hide()
{
    var x = document.getElementById('MyPreference');
    if (x.style.display === 'block') {
        x.style.display = 'none';
    } else {
        x.style.display = 'none';
    }
}
//
