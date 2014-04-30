
function addCourseCompare() {
	var allccs = document.getElementsByClassName("cc")
	numccs = allccs.length
	if (numccs>2) {
		alert("Sorry, you cannot compare more than three courses.")
	}
	else {
		var inputfield = document.createElement("INPUT");
		inputfield.setAttribute("type", "text")
		inputfield.setAttribute("name", "cc"+numccs.toString())
		inputfield.setAttribute("class", "inputbox cc")
		inputfield.setAttribute("placeholder", "course title")
		document.getElementById("cc_inputs").appendChild(inputfield)
		document.getElementById("cc_buttons").removeChild(document.getElementById("addcc"))
	}
}

function myTest() {
	alert("Testing!")
}



