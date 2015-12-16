var latitude = null
var longitude = null

if (navigator.geolocation) {
	console.log("Find location")
	navigator.geolocation.getCurrentPosition(showPosition, geoError)
}

function clicked(cb) {
	//If save location is checked then use this
	var x = cb.checked;
	var b = document.getElementById("hidden_location");
	if (x ) {
		console.log(x)
		console.log("Checked")
		if (latitude & longitude) {
			console.log("Save location")
		    console.log(latitude);
		    b.value = latitude+","+longitude;
		}
	} else {
		b.value = ""
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
	latitude = position.coords.latitude;
    longitude = position.coords.longitude; 
}