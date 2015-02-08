window.onload = function () {
	
	var frequencyChart1 = {  // HARDCODED CHART
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
	
	/* #### TEST CHART
	var frequencyChart = {
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

	$("td").click(function() { // gets the click on the tables of people 
		
		/* #### ignore for now -- future query generator
		var URL = ""; 
	  	
	  	var name = $(this).html();
	  	var time = "2015-02-06 19:00:00"; 		
	  	var location = "Baystate";				
		URL += encodeURI("ajax/name" + String(name)) //String(time) + "&location="+ String(location)); */

		$.getJSON("/check", function(result){
			 
			console.log(result);  // returns in this format{Tikka Masala Sauce: 414.6712645435273}
			
			i = 0;
			
			var dict ={}; // create new dictionary for formating it inside the chart
			
			for (var name in result){ //dynamically attaches items
				
				data = result[name];  // frequency value
				
				dict.y = data;  // appends freq. value to the dictionary's y value
				
				dict.label = String(name); // label gets changed to the food item name
				
				console.log("object", dict); // test whether the dictionary got created
				
				frequencyChart.data[0].dataPoints[i] = dict; // append the dictionary to the appropriate value
				i++;
			
			}; // for loop ends

		}); // json call ends
		
	}); // click ends

$("#frequency1").CanvasJSChart(frequencyChart1);
	

	
}
