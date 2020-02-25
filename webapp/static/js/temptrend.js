// Copyright (c) 2020 Zorglub42 {contact(at)zorglub42.fr}.
//
// All rights reserved. This program and the accompanying materials
// are made available under the terms of the Apache License, Version 2.0
// which accompanies this distribution, and is available at
// http://www.apache.org/licenses/LICENSE-2.0

var temperatureTrendDef = {
	formatter: formatters.round,
	sensor: "TEMP",
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
			
					// scales: {
					// 	yAxes: [{
					// 		ticks: {
					// 			beginAtZero: false
					// 		}
					// 	}]
					// },
					title: {
						text: "Température sur les 6 dernières heures",
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
			
					// scales: {
					// 	yAxes: [{
					// 		ticks: {
					// 			beginAtZero: false
					// 		}
					// 	}]
					// },
					title: {
						text: "Température sur la denière demi heure",
						display: true
			
					}
				}
			});
		}
	}
}

temperatureTrend = new sensorChart(temperatureTrendDef)