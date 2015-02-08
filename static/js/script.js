window.onload = function () {

	console.log("afddas");

	var frequencyChart = {
		
		title: {
			text: "Frequency Analysis"
		},
        
        animationEnabled: true,
		
		data: [
		{
			type: "bar", //change it to line, area, bar, pie, etc
			
			dataPoints: [
				{ y: 0.8, label: "tomato" },
				{ y: 0.6, label: "lettuce"},
				{ y: 0.1, label:"beef" },
				{ y: 0, label:"pork" },
			
			]
		}
		]
	};
	


	$("#frequency").CanvasJSChart(frequencyChart);
	$("#yumScore").CanvasJSChart(yumScore);
	//$("#tumScore").CanvasJSChart(options);


}