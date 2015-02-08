window.onload = function () {

	var values;

	
	var frequencyChart1 = {
		title: {
			text: "Frequency Analysis"
		},       
        animationEnabled: true,	
		data: [
				{
					type: "bar", //change it to line, area, bar, pie, etc
					
					dataPoints: [  {y: 3.656596708344897, label: "Vegan Pumpkin Bread"},
									{y: 3.637705166049602, label: "Mixed Green Salad"},
									{y: 3.647026497395958, label: "New England Clam Chowder"},
									{y: 3.659165472888237, label: "Cream of Vegetable Soup"},
								]
				}
			]
	};
	/*var frequencyChart = {
		title: {
			text: "Frequency Analysis"
		},       
        animationEnabled: true,	
		data: [
				{
					type: "bar", //change it to line, area, bar, pie, etc
					
					dataPoints: [  {y: 3.656596708344897, label: "Vegan Pumpkin Bread"},
									{y: 3.637705166049602, label: "Mixed Green Salad"},
									{y: 3.647026497395958, label: "New England Clam Chowder"},
									{y: 3.659165472888237, label: "Cream of Vegetable Soup"},
								]
				}
			]
	};*/


	console.log(frequencyChart1.data[0].dataPoints[2]);

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
			
			dict.y = data/10;
			
			dict.label = String(name);
			
			console.log("i",i);
			
			console.log("object", dict);
			
			frequencyChart.data[0].dataPoints[i] = dict;
			i++;
		
		};
		//$("#frequency").CanvasJSChart(frequencyChart);
		
		console.log(frequencyChart.data[0].dataPoints);
		
		

	});

	
});

$("#frequency1").CanvasJSChart(frequencyChart1);
	

	
}
