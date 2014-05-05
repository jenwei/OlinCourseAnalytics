var randdata = [
  {name: "Software Design",    value:  8},
  {name: "Real World Measurements",    value: 3 },
  {name: "Art of Approximation",     value: 15},
  {name: "UOCD",   value: 7},
  {name: "Linearity", value: 4},
  {name: "Computer Architecture",     value: 3}
];
/*d3.select(".chart")
	.selectAll("div")
		.data(data)
	.enter().append("div")
		.style("height", function(d) { return d * 10 + "px"; })
			.text(function(d) { return d; });*/
graph(randdata, 250, 270, "#chart1");
graph(randdata, 250, 270, "#chart2");
//graph(randdata, 250, 270, 2);

function graph(data, twidth, theight, div) {
	d3.select(div)
		.append("svg")
			.classed("chart", true);

	/*var totalwidth = 350,
		totalheight = 270;*/
	totalwidth = twidth;
	totalheight = theight;

	/*var x = d3.scale.linear()
	    .domain([0, d3.max(data)])
	    .range([height, 0]);*/

	/*var chart = d3.select(".chart")
	    .attr("width", width)
	    .attr("height", height);*/

	var margin = {top: 10, right: 10, bottom: 10, left: 10},
	    width = totalwidth - margin.left - margin.right,
	    height = totalheight - margin.top - margin.bottom,
	    barUnit = height/d3.max(data, function(d) { return d.value; });

	var y = d3.scale.linear()
	    .range([barUnit, 0]);

	var chart = d3.select(div+" .chart")
	    .attr("width", width + margin.left + margin.right)
	    .attr("height", height + margin.top + margin.bottom)
	  .append("g")
	    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

	var barWidth = width / data.length;

	var bar = chart.selectAll("g")
	    .data(data)
	  .enter().append("g")
	    .attr("transform", function(d, i) { return "translate(" + i * barWidth + ",0)"; });

	bar.append("rect")
		.attr("y", function(d) {return height + y(d.value);})
	    .attr("height", function(d) { return -y(d.value);})
	    .attr("width", barWidth - 1);

	bar.append("text")
	    .text(function(d) { 
	    	if (d.name=="Art of Approximation") {
	    		console.log(height+y(d.value));
	    		console.log(-y(d.value));
	    		console.log(this.getComputedTextLength());
	    	}
	    	if (-y(d.value)/d.name.length <10 && (height+y(d.value))/d.name.length <10) {
	    		console.log("YAY" + d.name)
	    		if (d.name.length>=10) {
	    			return d.name.substring(0, 9)+"..."; 
	    		}
	    		return d.name;
	    	}
	    	return d.name});

	bar.select("text")
	    .attr("x", function(d) {
	    	return barWidth/2;
	  	})
	    .attr("dy", ".75em")
		.attr("y", function(d) { 
			if (this.getComputedTextLength() +20 >-y(d.value)) {
				console.log(d.name);
	    		return height + y(d.value) - 2*this.getComputedTextLength()/3 -10;
	    	}
	    	else  {
	    		return height + y(d.value)/2;
	    	}
	    })
		.attr("writing-mode", "tb")
}



function wrap(text, width) {
  text.each(function() {
    var text = d3.select(this),
        words = text.text().split(/\s+/).reverse(),
        word,
        line = [],
        lineNumber = 0,
        lineHeight = 1.1, // ems
        y = text.attr("y"),
        dy = parseFloat(text.attr("dy")),
        tspan = text.text(null).append("tspan").attr("x", 0).attr("y", y).attr("dy", dy + "em");
    while (word = words.pop()) {
      line.push(word);
      tspan.text(line.join(" "));
      if (tspan.node().getComputedTextLength() > width) {
        line.pop();
        tspan.text(line.join(" "));
        line = [word];
        tspan = text.append("tspan").attr("x", 0).attr("y", y).attr("dy", ++lineNumber * lineHeight + dy + "em").text(word);
      }
    }
  });
}

