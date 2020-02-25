// Copyright (c) 2020 Zorglub42 {contact(at)zorglub42.fr}.
//
// All rights reserved. This program and the accompanying materials
// are made available under the terms of the Apache License, Version 2.0
// which accompanies this distribution, and is available at
// http://www.apache.org/licenses/LICENSE-2.0
var formatters = {
	identity: function(v){
		return(v)
	},
	round: function(v){
		if (v == null){
			return v
		}
		return Math.round(v)
	},
	fixed2: function(v){
		if (v == null){
			return v
		}
		return v.toFixed(2)
	},
	ms2knts: function(v){
		if (v == null){
			return v
		}
		return (v * 1.94384).toFixed(2)
	},
	ms2kmh: (v)=>{
		if (v == null){
			return v
		}
		return (v * 3.6).toFixed(2)

	}

}

async function fetchTrendData(sensor, fromOffset, groupInterval, modulus, chart, formatFunc){
	response = await fetch("api/sensors/" + sensor + "/values?fromOffset=-" + fromOffset + "&groupInterval=" + groupInterval).catch(error => { console.log(error)})
	if (typeof response !== "undefined" && response.status == 200) {
		data = await response.json()

		withMinMax = chart.data.datasets.length > 1

		chart.data.labels = []
		chart.data.datasets[0].data = []
		if (withMinMax){
			chart.data.datasets[1].data = []
			chart.data.datasets[2].data = []
		}
		data.values.forEach(
			element => {
				chart.data.labels.push(
					new Date(
						Date.parse(
							element.timestamp
						)
					).toLocaleTimeString()
						.substring(0, 5)
				)
				if (withMinMax){
					chart.data.datasets[0].data.push(formatFunc(element.min))
					chart.data.datasets[1].data.push(formatFunc(element.max))
					chart.data.datasets[2].data.push(formatFunc(element.mean))
				}else{
					chart.data.datasets[0].data.push(formatFunc(element.mean))
				}
			}
		);

		chart.update()
	}

}
async function loopFetchTrendData(sensor, fromOffset, groupInterval, modulus, chart, formatFunc, timeout){
	fetchTrendData(sensor, fromOffset, groupInterval, modulus, chart, formatFunc)
	setTimeout(
		()=> {fetchTrendData(sensor, fromOffset, groupInterval, modulus, chart, formatFunc)},
		timeout
	)
}

async function isCompassSupported(callback){
	response = await fetch("api/admin/compass/support").catch(error => { console.log(error)})
	if (typeof response !== "undefined" && response.status == 200){
		data = await response.json()
		supported = (data.status == "OK")
	}else{
		supported = false
	}
	callback(supported)
}

async function loopFetchInstantValues(gauges, timeout){
	response = await fetch("api/sensors/last").catch(error => { console.log(error)})
	if (typeof response !== "undefined" && response.status == 200){
		data = await response.json()
		gauges.speed.chart.value = preferences.speed.getFormatter()(data.windspeed.value) //formatters.ms2knts(data.windspeed.value)

		preferences.applyPref(gauges.speed.chart, preferences.speed.chartOptions.current)

		// gauges.speed.chart.options.units = preferences.speed.chartOptions.current.unit
		// gauges.speed.chart.options.minValue = preferences.speed.chartOptions.current.minValue
		// gauges.speed.chart.options.maxValue = preferences.speed.chartOptions.current.maxValue
		// gauges.speed.chart.options.majorTicks = preferences.speed.chartOptions.current.majorTicks
		// gauges.speed.chart.options.minorTicks = preferences.speed.chartOptions.current.minorTicks
		// gauges.speed.chart.options.highlightsWidth = preferences.speed.chartOptions.current.highlightsWidth
		
		gauges.pressure.chart.value = data.pressure.value
		gauges.compass.chart.value = data.windheading.value
		gauges.temperature.chart.value = data.temperature.value
		gauges.humidity.chart.value = data.humidity.value
		if (data.load.value != null){
			gauges.power.chart.value = data.load.value
			$("#" + gauges.power.id).show()
		}
	}
	response = await fetch("api/sensors/WIND_H/values?fromOffset=-5m&groupInterval=1d").catch(error => { console.log(error)})
	if (typeof response !== "undefined" &&response.status == 200){
		data = await response.json()
		if (data.values.length>0){
			gauges.compass.chart.options.highlights = [
				{
					"from": data.values[0].min,
					"to": data.values[0].max,
					"color": "rgba(0,0 ,120, 0.3)"
				}
			]
			gauges.compass.chart.update()
			}
	}
	response = await fetch("api/sensors/WIND_S/values?fromOffset=-5m&groupInterval=1d").catch(error => { console.log(error)})
	if (typeof response !== "undefined" &&response.status == 200){
		data = await response.json()
		if (data.values.length>0){
			formatter = preferences.speed.getFormatter()

			gauges.speed.chart.options.highlights = [
				{
					"from": formatter(data.values[0].min),
					"to": formatter(data.values[0].max),
					"color": "rgba(0,0 ,120, 0.3)"
				}
			]
			gauges.speed.chart.update()
		}
	}
	if (timeout != 0){
		setTimeout(
			()=>{loopFetchInstantValues(gauges, timeout)},
			timeout
		);
	}
}