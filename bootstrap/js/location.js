function clicked(cb) {
	//If save location is checked then use this
	var x = cb.checked;
	if (x ) {
		console.log(x)
		console.log("Checked")
		if (navigator.geolocation) {
			console.log("Navigator location")
			navigator.geolocation.getCurrentPosition(showPosition, geoError);
		} 
	}
}

var geoError = function(error) {
    console.log('Error occurred. Error code: ' + error.code);
    // error.code can be:
    //   0: unknown error
    //   1: permission denied
    //   2: position unavailable (error response from location provider)
    //   3: timed out
};

function showPosition(position) {
	//Get latitude and longiture and fill in the hidden input form
	var latitude = position.coords.latitude;
    var longitude = position.coords.longitude;
    var b = document.getElementById("hidden_location");
    console.log(latitude)
    b.value = latitude+","+longitude;
}