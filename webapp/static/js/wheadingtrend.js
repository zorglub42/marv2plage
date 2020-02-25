
var windHeadingTrendDef = {
	formatter: formatters.round,
	sensor: "WIND_H",
	trend6H: {
		chart: null,
		generateChart: function(canvasId, colors){
			var ctx = document.getElementById(canvasId);
			hLines = []
			for (i=0;i<=360; i+=10){
				if (i % 90 == 0){
					hLines.push(3)
				}else{
					hLines.push(1)
				}
			}
			this.chart = new Chart(ctx, {
				type: 'line',
				data: {
					labels: [],
					datasets: [
						{
							label: 'Min',
							data: [],
							fill: false,
							borderColor: colors[0].color,
							backgroundColor: colors[0].color.replace("1)","0.2)"),
						},
						{
							label: 'Max',
							data: [],
							fill: false,
							borderColor: colors[1].color,
							backgroundColor: colors[1].color.replace("1)","0.2)"),
						},
						{
							label: 'Moyenne',
							data: [],
							fill: false,
							borderColor: colors[2].color,
							backgroundColor: colors[2].color.replace("1)","0.2)"),
						},
					]
				},
				options: {
					legend: {
						display: true,
						labels: {
							boxWidth: 15,
						}
					},
			
					scales: {
						yAxes: [{
							ticks: {
								max : 360,    
								min : 0,
								stepSize: 10,
								callback:(value, index, values)=>{
									if (value % 45 == 0){
										return value + "°"
									}else{
										return ""
									}
								}
							},
							gridLines: {
								lineWidth: hLines
							}
						}]
					},
					title: {
						text: "Direction du vent sur les 6 dernières heures",
						display: true
			
					}
				}
			})
		},
	
	},
	trend30M: {
		chart: null,
		generateChart: function(canvasId, colors){
			var ctx = document.getElementById(canvasId);
			hLines = []
			for (i=0;i<=360; i+=10){
				if (i % 90 == 0){
					hLines.push(3)
				}else{
					hLines.push(1)
				}
			}
			this.chart = new Chart(ctx, {
				type: 'line',
				data: {
					labels: [],
					datasets: [
						{
							label: 'Min',
							data: [],
							fill: false,
							borderColor: colors[0].color,
							backgroundColor: colors[0].color.replace("1)","0.2)"),
						},
						{
							label: 'Max',
							data: [],
							fill: false,
							borderColor: colors[1].color,
							backgroundColor: colors[1].color.replace("1)","0.2)"),
						},
						{
							label: 'Moyenne',
							data: [],
							fill: false,
							borderColor: colors[2].color,
							backgroundColor: colors[2].color.replace("1)","0.2)"),
						},
					]
				},
				options: {
					legend: {
						display: true,
						labels: {
							boxWidth: 15,
						}
					},
			
					scales: {
						yAxes: [{
							ticks: {
								max : 360,    
								min : 0,
								stepSize: 10,
								callback: (value, index, values)=>{
									if (value % 45 == 0){
										return value + "°"
									}else{
										return ""
									}
								}
			
							},
							gridLines: {
								lineWidth: hLines
							}
						}]
					},
					title: {
						text: "Direction du vent sur la denière demi heure",
						display: true
			
					}
				}
			});
		}
	}
}

windHeadingTrend = new sensorChart(windHeadingTrendDef)