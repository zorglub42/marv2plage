// Copyright (c) 2020 Zorglub42 {contact(at)zorglub42.fr}.
//
// All rights reserved. This program and the accompanying materials
// are made available under the terms of the Apache License, Version 2.0
// which accompanies this distribution, and is available at
// http://www.apache.org/licenses/LICENSE-2.0
var sensors = {
	speed:{
		id: "WIND_S",
		lines: [
			{
				color: "rgba(54, 162, 235, 1)"
			},
			{
				color: "rgba(255, 206, 86, 1)"
			},
			{
				color: "rgba(255, 99, 132, 1)"
			}
		]
	},
	compass: {
		id: "WIND_H",
		lines:[
			{
				color: "rgba(54, 162, 235, 1)"
			},
			{
				color: "rgba(255, 206, 86, 1)"
			},
			{
				color: "rgba(255, 99, 132, 1)"
			}
		]
	},
	temperature: {
		id: "TEMP",
		lines:[
			{
				color: "rgba(2, 112, 38, 1)"
			}
		]
	},
	pressure: {
		id: "A_PRESS",
		lines:[
			{
				color: "rgba(229, 99, 0, 1)"
			}
		]
	},
	humidity: {
		id: "HUM",
		lines:[
			{
				color: "rgba(0, 39, 102, 1)"
			}
		]
	}
}

var chartsDef = {
	trend6H: {
		offset: "6h",
		grouptime: "10m",
		timeout: 120000,
	},
	trend30M: {
		offset: "30m",
		grouptime: "1m",
		timeout: 30000,
	},
	current: {
		timeout: 2500
	}
}
