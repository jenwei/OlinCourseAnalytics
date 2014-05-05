var tabdict = {"Course Search": "#sidebar #courseside", "Compare Courses":"#sidebar #compareside", "Advanced Search":"#sidebar #splitside"}

jQuery(function(){
	console.log("the sidebar js is running");
	$(".splitform").hide();
	$("#sidebar #courseside").hide();
	$("#sidebar #compareside").hide();
	$("#sidebar #splitside").hide();
	$("#sidebar").hide();
	//$(".center").hide();
	//alert("yo")

	$('#tabs a').click( function() {
		if($(tabdict[this.innerHTML]).is(":visible")) {
			$(tabdict[this.innerHTML]).hide();
			$("#sidebar").hide();
			/*$("#sidebar #courseside").hide();
			$("#sidebar #compareside").hide();
			$("#sidebar #splitside").hide();
			$("#sidebar").show()
			if(this.innerHTML=="Course Search") {
				$("#sidebar #courseside").show();
			}
			else if (this.innerHTML=="Compare Courses") {
				$("#sidebar #compareside").show();
			}
			else if (this.innerHTML=="Data Split") {
				$("#sidebar #splitside").show();
			}*/
		}
		else {
			$("#sidebar #courseside").hide();
			$("#sidebar #compareside").hide();
			$("#sidebar #splitside").hide();
			$("#sidebar").show('slow');
			$(tabdict[this.innerHTML]).show();
		}
		return false; 
	});

	$('#hidesidebar a').click(function() {
		$("#sidebar #courseside").hide();
		$("#sidebar #compareside").hide();
		$("#sidebar #splitside").hide();
		$("#sidebar").hide();
		return false;
	});

  	$('input').change(function () {

  		if(this.type=="checkbox" && this.className=="datasplitcb") {
			if(this.checked){
				if(this.value=="all"){
					all = $('input[type="checkbox"][name="'+this.name+'"]');
					for(i=1; i<all.length;i++) {
						if(all[i].checked==false) {
							all[i].checked = true;
							addSearchTag(all[i].value, '#allsearchtags ul');
						}
					}
				}	
				else {
					addSearchTag(this.value, '#allsearchtags ul');
				}
			}
			
			else {
				if(this.value!="all") {
					removeSearchTag(this.value, '#allsearchtags ul')
				}
			}

		}


		else if (this.type=="radio" && this.name=="dsby") {
			$(".splitform").hide();
			if(this.value=="major") {
				$('#majorsplitform').show('slow');
			}
			if(this.value=="color"){
				$('#colorsplitform').show('slow');
			}
		}
  	});
});

function addSearchTag(innerhtml, location) {
	var newtag = document.createElement('LI');
	newtag.innerHTML = innerhtml;
	newtag.id = innerhtml.replace(" ", "");
	//alert(newtag.id);
	$(location).append(newtag);
} 

function removeSearchTag(innerhtml, location) {
	var tag = "#"+innerhtml.replace(" ", "");
	//alert(tag);
	$(tag).remove();
}



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
