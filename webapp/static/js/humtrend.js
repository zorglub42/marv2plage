
var humidityTrendDef = {
	formatter: formatters.round,
	sensor: "HUM",
	trend6H: {
		chart: null,
		generateChart: function(canvasId, colors){
			var ctx = document.getElementById(canvasId);
			this.chart = new Chart(ctx, {
				type: 'line',
				data: {
					labels: [],
					datasets: [
						{
							label: 'Moyenne',
							data: [],
							fill: true,
							borderColor: colors[0].color,
							backgroundColor: colors[0].color.replace("1)","0.2)"),
						},
					]
				},
				options: {
					legend: {
						display: false,
						labels: {
							boxWidth: 15,
						}
					},
			
					scales: {
						yAxes: [{
							ticks: {
								beginAtZero: true,
								max: 100
							}
						}]
					},
					title: {
						text: "Humidité sur les 6 dernières heures",
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
			this.chart = new Chart(ctx, {
				type: 'line',
				data: {
					labels: [],
					datasets: [
						{
							label: 'Moyenne',
							data: [],
							fill: true,
							borderColor: colors[0].color,
							backgroundColor: colors[0].color.replace("1)","0.2)"),
						},
					]
				},
				options: {
					legend: {
						display: false,
						labels: {
							boxWidth: 15,
						}
					},
			
					scales: {
						yAxes: [{
							ticks: {
								beginAtZero: true,
								max: 100
							}
						}]
					},
					title: {
						text: "Humidité sur la denière demi heure",
						display: true
			
					}
				}
			});
		}
	}
}

humidityTrend = new sensorChart(humidityTrendDef)