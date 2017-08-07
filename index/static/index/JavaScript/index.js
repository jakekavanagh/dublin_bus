function populate(route, dict, locations) {
     route = route;
     var zero = [dict[route]['0']];
     var one = [dict[route]['1']];
     var all_stops = zero.concat(one);

     var array = JSON.parse("["+all_stops+"]");
     <!--array.sort(function(a, b){return a-b});-->
     var dropdown = document.getElementById("origin");
     while (dropdown.options.length > 0) {
        dropdown.remove(0);
    }
     var option = document.createElement("option");
     option.text = "Select an Origin Stop";
     dropdown.add(option);

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

