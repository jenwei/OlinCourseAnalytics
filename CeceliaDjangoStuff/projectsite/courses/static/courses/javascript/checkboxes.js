
jQuery(function(){
	$(".splitform").hide();

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




