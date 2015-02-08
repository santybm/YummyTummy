window.onload = function () {

	var values;

	
	var frequencyChart = {
		title: {
			text: "Frequency Analysis"
		},       
        animationEnabled: true,	
		data: [
				{
					type: "bar", //change it to line, area, bar, pie, etc
					
					dataPoints: [ 
								]
				}
			]
	};

	$("td").click(function() {
		var URL = "";
	  	
	  	var name = $(this).html();
	  	var time = "2015-02-06 19:00:00"; 		// time and location are hardcoded in
	  	var location = "Baystate";				// can later create input options
	  
		URL += encodeURI("ajax/name" + String(name)) //String(time) + "&location="+ String(location));

	$.getJSON("/check", function(result){
		 
		console.log(result);  //{ Tikka Masala Sauce: 414.6712645435273}
		//foo = $.parseJSON(result);
		//console.log(foo);
		i = 0;
		var dict ={};
		
		for (var name in result){ //dynamically attaches items
			
			data = result[name];
			dict.x = i;
			
			dict.y = data;
			
			dict.label = String(name);
			console.log("i",i);
			console.log("label", data);
			console.log("object", dict);
			
			frequencyChart.data[0].dataPoints[i] = dict;
			i++;
		
		};
		console.log(frequencyChart.data[0].dataPoints);
		$("#frequency").CanvasJSChart(frequencyChart);

	});
	
});


	

	
}
