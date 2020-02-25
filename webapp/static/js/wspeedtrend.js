// Copyright (c) 2020 Zorglub42 {contact(at)zorglub42.fr}.
//
// All rights reserved. This program and the accompanying materials
// are made available under the terms of the Apache License, Version 2.0
// which accompanies this distribution, and is available at
// http://www.apache.org/licenses/LICENSE-2.0

var windSpeedTrendDef = {
	//formatter: formatters.ms2knts,
	formatter: preferences.speed.format,
	sensor: "WIND_S",
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
								min: 0
							}
						}],
						xAxes: [
							{
								ticks: {
									//autoSkip: true,
									maxTicksLimit: 6
								}
							}							
						]
					},
					title: {
						text: "Vitesse du vent sur les 6 dernières heures",
						display: true,
			
					}
				}
			});
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
								min: 0
							}
						}],
						xAxes: [
							{
								ticks: {
									autoSkip: true,
									maxTicksLimit: 5
								}
							}							
						]
					},
					title: {
						text: "Vitesse du vent sur la denière demie heure",
						display: true
			
					}
				}
			});
		}
	}
}

windSpeedTrend = new sensorChart(windSpeedTrendDef)