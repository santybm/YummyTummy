window.onload = function () {
	
	var frequencyChart = {  // HARDCODED CHART
		title: {
			text: "Frequency Analysis: Items That Will Be Suggested"
		},       
        animationEnabled: true,	
		data: [
				{
					type: "bar", //change it to line, area, bar, pie, etc
					
					dataPoints: [  {y: 365.6596708344897, label: "Vegan Pumpkin Bread"},
				{y: 363.7705166049602, label: "Mixed Green Salad"},
				{y: 364.7026497395958, label: "New England Clam Chowder"},
				{y: 365.9165472888237, label: "Cream of Vegetable Soup"} 	
								]
				}
			]
	};

	var leastFav =  [   {y: 1.3061434291868934, label:"Flakes"}, 
						{y:  4.587799086540939, label:"Crushed Red Pepper"},
						{y: 1.9853447653678495, label: "Chipotle Peppers in Adobo Sauce"},
						{y: 1.9621285686526527, label: "Sage"},
						{y: 1.4583840787218189, label: "American Cheese Sliced"}
					]

		$("#frequency").CanvasJSChart(frequencyChart);
	
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
	var bad=true;

	mostFav = [{y: 365.6596708344897, label: "Vegan Pumpkin Bread"},
				{y: 363.7705166049602, label: "Mixed Green Salad"},
				{y: 364.7026497395958, label: "New England Clam Chowder"},
				{y: 365.9165472888237, label: "Cream of Vegetable Soup"} ]

	$("#button").click(function() { // gets the click on the tables of people 
		
		console.log(bad);
		
		if(bad==true){
			frequencyChart.title.text = "Frequency Analysis: Items That Will NEVER Be Suggested"
			frequencyChart.data[0].dataPoints = leastFav;
			$("#frequency").CanvasJSChart(frequencyChart);
			bad = false;
		}else if(bad == false){
			frequencyChart.title.text = "Frequency Analysis: Items That Will Be Suggested"
			frequencyChart.data[0].dataPoints = leastFav;
			bad = true;
		}
	
	});


		/*var name = $(this).html();
		
		dict_names.add(name);

		console.log(dict_names);*/



		/* #### ignore for now -- future query generator
		var URL = ""; 
	  	
	  	;
	  	var time = "2015-02-06 19:00:00"; 		
	  	var location = "Baystate";				
		URL += encodeURI("ajax/name" + String(name)) //String(time) + "&location="+ String(location)); */

		/*$.getJSON("/check", function(result){
			 
			console.log(result);  // returns in this format{Tikka Masala Sauce: 414.6712645435273}
			
			i = 0;
			
			var dict ={}; // create new dictionary for formating it inside the chart
			
			/*for (var name in result){ //dynamically attaches items
				
				data = result[name];  // frequency value
				
				dict.y = data;  // appends freq. value to the dictionary's y value
				
				dict.label = String(name); // label gets changed to the food item name
				
				console.log("object", dict); // test whether the dictionary got created
				
				frequencyChart.data[0].dataPoints[i] = dict; // append the dictionary to the appropriate value
				i++;
			
			}; // for loop ends*/
			 // json call ends
		
	}; // click ends	


