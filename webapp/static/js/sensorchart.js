// Copyright (c) 2020 Zorglub42 {contact(at)zorglub42.fr}.
//
// All rights reserved. This program and the accompanying materials
// are made available under the terms of the Apache License, Version 2.0
// which accompanies this distribution, and is available at
// http://www.apache.org/licenses/LICENSE-2.0
class sensorChart{
	

	constructor(chartDef) {
		this.chartDef = chartDef
	}

	start(canvasId6H, canvasId30M, settings, sensor){
		this.settings = settings
		this.chartDef.sensor = sensor.id
		this.chartDef.trend6H.generateChart(canvasId6H, sensor.lines)
		this.chartDef.trend30M.generateChart(canvasId30M, sensor.lines)


		this.chartDef.trend6H.chart.options.scales.xAxes[0].ticks.autoSkip = true
		this.chartDef.trend30M.chart.options.scales.xAxes[0].ticks.autoSkip = true

		// this.chartDef.trend6H.chart.options.title.fontSize = 35
		// this.chartDef.trend30M.chart.options.title.fontSize = 35
		this.chartDef.trend6H.chart.options.maintainAspectRatio = false;
		this.chartDef.trend30M.chart.options.maintainAspectRatio = false;

		this.chartDef.trend6H.chart.options.responsive = true;
		this.chartDef.trend30M.chart.options.responsive = true;
	


		this.chartDef.trend6H.chart.options.scales.xAxes[0].ticks.maxTicksLimit = 6
		this.chartDef.trend30M.chart.options.scales.xAxes[0].ticks.maxTicksLimit = 5

		this.chartDef.trend30M.chart.data.datasets.forEach(dataset => {
			dataset.backgroundColor = dataset.backgroundColor.replace("1)","0.2)") 
		});
		this.chartDef.trend6H.chart.data.datasets.forEach(dataset => {
			dataset.backgroundColor = dataset.backgroundColor.replace("1)","0.2)") 
		});

		loopFetchTrendData(
			this.chartDef.sensor,
			settings.trend6H.offset,
			settings.trend6H.grouptime,
			settings.trend6H.modulus,
			this.chartDef.trend6H.chart,
			this.chartDef.formatter,
			settings.trend6H.timeout
		)
		loopFetchTrendData(
			this.chartDef.sensor,
			settings.trend30M.offset,
			settings.trend30M.grouptime,
			settings.trend30M.modulus,
			this.chartDef.trend30M.chart,
			this.chartDef.formatter,
			settings.trend30M.timeout
		)
	}
	reload(){
		fetchTrendData(
			this.chartDef.sensor,
			this.settings.trend6H.offset,
			this.settings.trend6H.grouptime,
			this.settings.trend6H.modulus,
			this.chartDef.trend6H.chart,
			this.chartDef.formatter
		)
		fetchTrendData(
			this.chartDef.sensor,
			this.settings.trend30M.offset,
			this.settings.trend30M.grouptime,
			this.settings.trend30M.modulus,
			this.chartDef.trend30M.chart,
			this.chartDef.formatter
		)
	}

}