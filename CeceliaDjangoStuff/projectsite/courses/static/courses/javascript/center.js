centerpages = {"doSearch":"#coursecenter", "compare":"#comparecenter", "advancedSearch": "#splitcenter", "start": "#instructions"}

jQuery(function() {
	//console.log("the center js is running");
	for (var key in centerpages) {
		$("#center "+centerpages[key]).hide();
	}
	//$("#center").hide();
	var path=location.pathname;
	pathparts = path.substring(1, path.length-1).split("/")
	//alert(pathparts);
	//alert(typeof pathparts[2])
	if (typeof pathparts[1]!= undefined && typeof centerpages[pathparts[1]]!=undefined) {
		$("#center "+centerpages[pathparts[1]]).show();		
	
	} 
});

function replaceAll(find, replace, str) {
  return str.replace(new RegExp(find, 'g'), replace);
}