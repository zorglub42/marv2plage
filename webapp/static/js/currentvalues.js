var currentValues = {
	speed: {
		chart: null,
		id: null,
		generateChart: function(canvasId){
			this.id = canvasId
			this.chart = new RadialGauge({
				renderTo: canvasId,
				minValue: 0,
				maxValue: 45,
				majorTicks: [
					0,
					5,
					10,
					15,
					20,
					25,
					30,
					35,
					40,
					45
				],
				minorTicks: 5,
				highlightsWidth: 30,
				highlights: [
				// {
				// 		"from": "0",
				// 		"to": "15",
				// 		"color": "rgba(0,120 ,0, 0.3)"
				// 	},
				// 	{
				// 		"from": "15",
				// 		"to": "30",
				// 		"color": "rgb(255,140,0, 0.3)"
				// 	},
				// 	{
				// 		"from": "30",
				// 		"to": "45",
				// 		"color": "rgb(255,0 ,0, 0.3)"
				// 	},
				],
				valueBox: true,
				valueInt: 0,
				valueDec: 2,
				units: "knts",
				animationDuration: 1500,
				animationRule: "linear",
				borderOuterWidth: 20,
				colorBorderOuter: "#ccc",
				colorBorderOuterEnd: "#000",
				colorPlate: "#fff",
				colorPlateEnd: "#c5c8cc",
				colorPlate: "#fff",
				colorPlateEnd: "#c5c8cc",
			}).draw();
		}
	},
	compass: {
		chart: null,
		id: null,
		generateChart: function(canvasId){
			this.id = canvasId
			this.chart = new RadialGauge({
				renderTo: canvasId,
				minValue: 0,
				maxValue: 360,
				majorTicks: [
					"N",
					"NE",
					"E",
					"SE",
					"S",
					"SW",
					"W",
					"NW",
					"N"
				],
				minorTicks: 9,
				ticksAngle: 360,
				startAngle: 180,
				strokeTicks: false,
				highlights: false,
				colorPlate: "rgba(170, 51, 51, 1)",
				colorMajorTicks: "#f5f5f5",
				colorMinorTicks: "#ddd",
				colorNumbers: "#ccc",
				colorNeedle: "rgba(240, 128, 128, 1)",
				colorNeedleEnd: "rgba(255, 160, 122, .9)",
				valueBox: false,
				valueTextShadow: false,
				// colorCircleInner: "#fff",
				// colorNeedleCircleOuter: "#ccc",
				// needleCircleSize: 15,
				// needleCircleOuter: false,
				animationRule: "linear",
				needleType: "line",
				needleStart: 60,
				needleEnd: 90,
				needleWidth: 3,
				borders: true,
				// borderInnerWidth: 0,
				// borderMiddleWidth: 0,
				borderOuterWidth: 20,
				colorBorderOuter: "#ccc",
				colorBorderOuterEnd: "#000",
				colorNeedleShadowDown: "#222",
				borderShadowWidth: 0,
				animationDuration: 1500,
				value: 270,
				highlightsWidth: 80,
				// animationTarget: "plate"
			}).draw()
		}
	},
	temperature: {
		chart: null,
		id: null,
		generateChart: function(canvasId){
			this.id = canvasId
			this.chart = new RadialGauge({
				renderTo: canvasId,
				minValue: -10,
				maxValue: 50,
				majorTicks: [
					-10,
					-5,
					0,
					5,
					10,
					15,
					20,
					25,
					30,
					35,
					40,
					45,
					50
				],
				minorTicks: 5,
				valueBox: true,
				valueInt: 1,
				valueDec: 0,
				units: "°C",
				animationDuration: 1500,
				animationRule: "linear",
				highlightsWidth: 30,
				highlights: [
				{
						"from": "-10",
						"to": "0",
						"color": "rgba(120,0,120, 0.3)"
					},
					{
						"from": "0",
						"to": "10",
						"color": "rgba(0,0,255, 0.3)"
					},
					{
						"from": "10",
						"to": "20",
						"color": "rgb(0,120,0, 0.3)"
					},
					{
						"from": "20",
						"to": "30",
						"color": "rgba(255,255,0, 0.3)"
					},
					{
						"from": "30",
						"to": "40",
						"color": "rgb(255,140,0, 0.3)"
					},
					{
						"from": "40",
						"to": "50",
						"color": "rgb(255,0,0, 0.3)"
					},
				],
				borderOuterWidth: 20,
				colorBorderOuter: "#ccc",
				colorBorderOuterEnd: "#000",
				colorPlate: "#fff",
				colorPlateEnd: "#c5c8cc",
			}).draw()
		}
	},
	pressure: {
		chart: null,
		id: null,
		generateChart: function(canvasId) {
			this.id = canvasId
			this.chart = new RadialGauge({
				renderTo: canvasId,
				value: 950,
				minValue: 950,
				maxValue: 1050,
				majorTicks: [
					950,
					975,
					1000,
					1025,
					1050,
				],
				minorTicks: 5,
				valueBox: true,
				valueInt: 1,
				valueDec: 0,
				units: "hPa",
				animationDuration: 1500,
				animationRule: "linear",
				highlights: false,
				borderOuterWidth: 20,
				colorBorderOuter: "#ccc",
				colorBorderOuterEnd: "#000",
				colorPlate: "#fff",
				colorPlateEnd: "#c5c8cc",
			}).draw()
		}
	},
	humidity: {
		chart: null,
		id: null,
		generateChart: function(canvasId) {
			this.id = canvasId
			this.chart = new RadialGauge({
				renderTo: canvasId,
				minValue: 0,
				maxValue: 100,
				majorTicks: [
					0,
					10,
					20,
					30,
					40,
					50,
					60,
					70,
					80,
					90,
					100,
				],
				highlightsWidth: 30,
				highlights: [
					{
						"from": 0,
						"to": 25,
						"color": "rgba(0, 39, 102, 0.1)"
					},
					{
						"from": 25,
						"to": 50,
						"color": "rgba(0, 39, 102, 0.3)"
					},
					{
						"from": 50,
						"to": 75,
						"color": "rgba(0, 39, 102, 0.5)"
					},
					{
						"from": 75,
						"to": 100,
						"color": "rgba(0, 39, 102, 0.7)"
					},

				],
				valueBox: true,
				valueInt: 1,
				valueDec: 0,
				units: "%",
				animationDuration: 1500,
				animationRule: "linear",
				borderOuterWidth: 20,
				colorBorderOuter: "#ccc",
				colorBorderOuterEnd: "#000",
				colorPlate: "#fff",
				colorPlateEnd: "#c5c8cc",
			}).draw()
		}
	},
	power: {
		chart: null,
		id: null,
		generateChart: function(canvasId) {
			this.id = canvasId
			this.chart = new RadialGauge({
				renderTo: canvasId,
				minValue: 0,
				maxValue: 100,
				startAngle: 110,
				ticksAngle: 140,
				majorTicks: [
					0,
					25,
					50,
					75,
					100,
				],
				minorTicks: 0,
				highlightsWidth: 40,
				highlights: [
					{
						"from": 0,
						"to": 25,
						"color": "rgba(255, 0, 0, 0.8)"
					}				],
				valueBox: true,
				valueInt: 1,
				valueDec: 0,
				animationDuration: 1500,
				animationRule: "linear",
				borderOuterWidth: 3,
				colorBorderOuter: "#ccc",
				colorBorderOuterEnd: "#000",
				colorPlate: "rgba(0, 0, 0)",
				colorPlateEnd: "rgba(50, 50, 50)",
				colorMajorTicks: "#ddd",
				colorNumbers: "#eee",
				needleEnd: 60,
				valueBox: false,
				units: "Batt.",
				fontNumbersSize: "0",
				fontUnitsSize: "50",
				colorUnits: "#fff",
				highlightsWidth: 15
			}).draw()
		}
	},
	start: function(compassCanvasId, speedCanvasId, temperatureCanvasId, humidityCanvasId, pressureCanvasId, powerCanvasId, settings){
		this.compass.generateChart(compassCanvasId)
		this.speed.generateChart(speedCanvasId)
		this.temperature.generateChart(temperatureCanvasId)
		this.pressure.generateChart(pressureCanvasId)
		this.humidity.generateChart(humidityCanvasId)
		this.power.generateChart(powerCanvasId)

		loopFetchInstantValues(this, settings.current.timeout)
	}
}
