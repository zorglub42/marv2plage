// Copyright (c) 2020 Zorglub42 {contact(at)zorglub42.fr}.
//
// All rights reserved. This program and the accompanying materials
// are made available under the terms of the Apache License, Version 2.0
// which accompanies this distribution, and is available at
// http://www.apache.org/licenses/LICENSE-2.0

var preferences = {
	wifiClientCount: 3,
	curWifiClient: 0,
	showWifiNeighborhood: (client_id) => {
		preferences.curWifiClient = client_id
		$('#wifiNetworks').modal('show');$('#settings').modal('hide');
	},
	getPrefs: () =>{
		json = getCookie("ffbc8meteo")
		if (json == ""){
			return null
		}
		return JSON.parse(json)
	},
	setPrefs: (prefs) =>{
		setCookie("ffbc8meteo", JSON.stringify(prefs), 365)
	},
	applyPref: (chart, pref) =>{
		chart.options.units = pref.unit
		chart.options.minValue = pref.minValue
		chart.options.maxValue = pref.maxValue
		chart.options.majorTicks = pref.majorTicks
		chart.options.minorTicks = pref.minorTicks
		chart.options.highlightsWidth = pref.highlightsWidth

	},
	speed: {
		setUnit: (unit) => {
			prefs = preferences.getPrefs()
			if (prefs == null){
				prefs = {speed: "knts"}
			}
			prefs.speed = unit
			preferences.setPrefs(prefs)
			loopFetchInstantValues(currentValues, 0)
			windSpeedTrend.reload()

		},
		chartOptions: {
			knts: {
				id: "knts",
				unit: "knts",
				minValue: 0,
				maxValue: 40,
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
					// 45
				],
				minorTicks: 5,
				highlightsWidth: 30
			},
			kmh: {
				id: "kmh",
				unit: "km/h",
				minValue: 0,
				maxValue: 100,
				majorTicks: [
					0,
					20,
					40,
					60,
					80,
					100
				],
				minorTicks: 10,
				highlightsWidth: 60
			},
			ms: {
				id: "ms",
				unit: "m/s",
				minValue: 0,
				maxValue: 50,
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
					45,
					50
				],
				minorTicks: 5,
				highlightsWidth: 30
			},
			current: null
		},
		getFormatter: () => {
			prefs = preferences.getPrefs()
			if (prefs != null && prefs.speed !== undefined){
				if (prefs.speed == "ms"){
					preferences.speed.chartOptions.current = preferences.speed.chartOptions.ms
					fmt = formatters.fixed2
				}else if (prefs.speed == "kmh"){
					preferences.speed.chartOptions.current = preferences.speed.chartOptions.kmh
					fmt = formatters.ms2kmh
				}else if (prefs.speed == "knts"){
					preferences.speed.chartOptions.current = preferences.speed.chartOptions.knts
					fmt = formatters.ms2knts
				}else{
					preferences.speed.chartOptions.current = preferences.speed.chartOptions.knts
					fmt = formatters.ms2knts
				}

			}else{
				preferences.speed.chartOptions.current = preferences.speed.chartOptions.knts
				fmt = formatters.ms2knts
			}
			$('input:radio[name="speedUnit"]').filter('[value=' + preferences.speed.chartOptions.current.id + ']').attr('checked', true);
			return fmt
		},
		format: (v) => {
			return preferences.speed.getFormatter()(v)
		}
	
	},
	hideAllSettings: () =>{
		$('#compassSettings').hide()
		$('#speedUnitSettings').hide()
		$('#wifiSettings').hide()
	},
	compassSettings: ()=>{
		preferences.hideAllSettings()
		$('#compassSettings').show()

	},
	speedUnitSettings: ()=>{
		preferences.hideAllSettings()
		$('#speedUnitSettings').show()

	},
	revealPassword: (field) =>{
		$(field).attr('type','input');
		setTimeout(
			() =>{
				$(field).attr('type','password')

			},
			5000
		)

	},
	wifiSettings: async ()=>{
		preferences.hideAllSettings()
		$('#hotspotPASS').attr('type','password')
		for (i=0;i<preferences.wifiClientCount;i++){
			$('#clientPASS' + i).attr('type','password')
		}
		$('#wifiSettings').show()
		resp = await fetch("api/admin/system/wifi").catch(
			error => { console.log(error)}
		)
		if (typeof resp !== "undefined" && resp.status == 200) {
			data = await resp.json()
			table=document.getElementById("data");
			rowPattern=document.getElementById("rowTpl");
			table.innerHTML=''

			ssidList = data.networks
			for (i=0;i<ssidList.length;i++){

				
				newRow=rowPattern.cloneNode(true);
				newRow.removeAttribute('id');
				newRow.removeAttribute('style');
				newRow.innerHTML=newRow.innerHTML.replaceAll("{ssidList[i].ssid}", ssidList[i].ssid)
												 .replaceAll("{ssidList[i].quality}", ssidList[i].quality);
				table.appendChild(newRow);
			}
			table.appendChild(rowPattern)
			$('input:radio[name="wifiMode"]').filter('[value=' + data.mode + ']').attr('checked', true);
			preferences.checkWifiMode()
			$('#hotspotSSID').val(data.hotspot.ssid)
			$('#hotspotPASS').val(data.hotspot.passphrase)
			for (i=0;i<data.client.length;i++){
				$('#clientSSID' + i).val(data.client[i].ssid)
				$('#clientPASS' + i).val(data.client[i].passphrase)
			}
			$("#mac").html(data.mac)
			
		}else{
			console.log("C'est tout Peuteu !!!")
		}

	},
	setClientSSID: (ssid)=>{
		$("#clientSSID" + preferences.curWifiClient).val(ssid)
		$('#settings').modal('show');
		$('#wifiNetworks').modal('hide');
	},
	checkWifiMode: ()=>{
		$('input[name=wifiMode]:checked', '#frmWifiSettings').val()=="client"?$("#clientModeSettings").show():$("#clientModeSettings").hide()
	},
	saveWifiSettings: () =>{
		admin.applyWifi()
		$('#settings').modal('hide');
		alert("La station est en train de se reconnecter")
	}

}