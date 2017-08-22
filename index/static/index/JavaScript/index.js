//Function that allow origin stop dropdown to become populated from JSON data
function populate(route, dict, locations) {
    route = route;
    var zero = [dict[route]['0']];
    var one = [dict[route]['1']];

    if (zero == '') {
        all_stops = one;
    } else if (one == '') {
        all_stops = zero;
    } else {
        all_stops = zero.concat(one);
    }

    var array = JSON.parse("[" + all_stops + "]");
    var dropdown = document.getElementById("origin");

    while (dropdown.options.length > 0) {
        dropdown.remove(0);
    }

    var option = document.createElement("option");
    option.text = "Select an Origin Stop";
    dropdown.add(option);
    for (var i = 0; i < array.length; ++i) {
        var option = document.createElement("option");
        option.text = locations[array[i]]['name'] + ' - ' + array[i];
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

//Function that allow destination stop dropdown to become populated from JSON data
function populateDestination(start, dict, locations) {
    var route = document.getElementById("RouteNumbers").value;
    var subset;
    if ($.inArray(start, dict[route]['0']) != -1) {
        subset = dict[route]['0'].slice($.inArray(start, dict[route]['0']) + 1, );
    }
    if ($.inArray(start, dict[route]['1']) != -1) {
        var temp = dict[route]['1'].slice($.inArray(start, dict[route]['1']) + 1, );
        if (typeof subset == 'undefined') {
            subset = temp;
        } else {
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
        option.text = locations[subset[i]]['name'] + ' - ' + subset[i];
        option.value = subset[i];
        dropdown.add(option);
    }
}

//Save the user's selected values with localStorage to 'remember' the user's preference
function saveValues() {
    var routevalue = document.getElementById("RouteNumbers");
    var originvalue = document.getElementById("origin");
    var destinationvalue = document.getElementById("destination");
    localStorage._route = routevalue.value;
    localStorage._origin = originvalue.value;
    localStorage._destination = destinationvalue.value;
}

//Loads the user's previously selected inputs as a suggestion to search again
function loadValues() {
    var locations;
    $.getJSON("../../static/index/lats_and_longs.json", function(json) {
        locations = json;
        var route = localStorage._route;
        var origin = localStorage._origin;
        var destination = localStorage._destination;
        var x = document.getElementById('MyPreference');
        if (route == null || origin == "Select an Origin Stop") {
            x.style.display = 'none';
        } else {
            if (x.style.display === 'none') {
                x.style.display = 'block';
            }
            var title_string;
            if (origin == destination) {
                title_string = '';
            } else {
                title_string = ' to ' + '<b>' + locations[destination]['name'] + '</b>';
            }
            var title = 'You\'ve been here before! Would you like to search route ' + '<b>' + route + '</b> from <b>' + locations[origin]['name'] + '</b>' + title_string + ' again?';
            var result = '<input name = "orig" type ="hidden" value="' + origin + '"+/>' + '<input name = "dest" type ="hidden" value="' + destination + '"+/>' + '<input name = "route" type="hidden" value="' + route + '" />';
            document.getElementById('title').innerHTML = title;
            document.getElementById('fillForm').innerHTML = result;
        }
    });
}

//If no route was selected before, hide the suggestion div.
function No_Hide() {
    var x = document.getElementById('MyPreference');
    if (x.style.display === 'block') {
        x.style.display = 'none';
    } else {
        x.style.display = 'none';
    }
}