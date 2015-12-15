function clicked(cb) {
	//If save location is checked then use this
	var x = cb.checked;
	if (x ) {
		console.log(x)
		console.log("Checked")
		if (navigator.geolocation) {
			console.log("Navigator location")
			navigator.geolocation.getCurrentPosition(showPosition);
		} 
	}
}

function showPosition(position) {
	//Get latitude and longiture and fill in the hidden input form
	var latitude = position.coords.latitude;
    var longitude = position.coords.longitude;
    var b = document.getElementById("hidden_location");
    b.value = latitude+","+longitude;
}