// Copyright (c) 2020 Zorglub42 {contact(at)zorglub42.fr}.
#
// All rights reserved. This program and the accompanying materials
// are made available under the terms of the Apache License, Version 2.0
// which accompanies this distribution, and is available at
// http://www.apache.org/licenses/LICENSE-2.0
var admin = {
	reboot_timeout: 20000,
	shutdown: () =>{
		payload = {
			"command": "shutdown"
		}
		fetch(
			"api/admin/system",
			{
				method: 'POST',
				body: JSON.stringify(payload),
				headers: new Headers({'content-type': 'application/json'})
			}
		)
		admin.waitEnd()
		$("#modalContent").html("La station météo est en train de s'arrêter, faut attendre un peu....")
		return false
	},
	reboot: () => {
		payload = {
			"command": "reboot"
		}
		fetch(
			"api/admin/system",
			{
				method: 'POST',
				body: JSON.stringify(payload),
				headers: new Headers({'content-type': 'application/json'})
			}
		)
		$("#modalContent").html("La station météo est en train de redémarer")
		setTimeout(
			admin.reload,
			admin.reboot_timeout
		)
	return false
	},
	waitEnd: () => {
		fetch("api/admin/ping").then(
			(reponse)=> {
				setTimeout(
					admin.waitEnd,
					admin.reboot_timeout
				)
			}
		).catch(
			error => {
				setTimeout(
					() => {
						$("#modalContent").html("<strong>Tu peux debrancher la bêêêêête !!!!<strong>")
					},
					admin.reboot_timeout
				)
			}
		)
	},
	reload:  () => {
			fetch("api/admin/ping").then(
				(response) => {
					if (response.status == 200) {
						document.location.reload(true);
					}else{
						setTimeout(
							admin.reload,
							admin.reboot_timeout
						)
					} 
		
				}
			).catch( error =>{
				console.log(error)
				setTimeout(
					admin.reload,
					admin.reboot_timeout
				)
	})
	},
	settings: () => {
		$('#advance').modal('hide');
		$('#settings').modal('show');

	},
	hideSettingsResult: ()=>{
		window.setTimeout(
			() => {
				$("#settingsResult").html("")
				$("#settingsResultPanel").hide()
			},
			10000
		)
	},
	calibrateMag: async () => {
		$("#settingsResult").html("Aie l'air malin et va faire bouger le block girouette dans tous les sens")
		$("#settingsResultPanel").show()

		response = await fetch(
			"api/admin/compass/calibration",
			{
				method: "POST"
			}
		).catch(
			error => { console.log(error)}
		)
		if (typeof response !== "undefined" && response.status == 200) {
			data = await response.json()
			$("#settingsResult").html("Voila c'est fait, maintenant n'oublie pas de recaler le nord..." )
			
		}else{
			$("#settingsResult").html("C'est tout Peuteu !!!")
		}
		admin.hideSettingsResult()

	},
	findNorth: async () => {
		$("#settingsResult").html("Bah v'la... on a encore perdu le nord et c'est à moi de m'y coller....")
		$("#settingsResultPanel").show()

		response = await fetch(
			"api/admin/compass/north-finder",
			{
				method: "POST"
			}
		).catch(
			error => { console.log(error)}
		)
		if (typeof response !== "undefined" && response.status == 200) {
			data = await response.json()
			$("#settingsResult").html("Et v'la !! La girouette est de base orientée au " + data.message.replace("MAG SHIFT", "") )
			
		}else{
			$("#settingsResult").html("C'est tout Peuteu !!!")
		}
		admin.hideSettingsResult()

	},
	setTime: async () => {
		curDate = new Date()
		payload = {
			dateTime: curDate.toISOString()
		}
		resp = await fetch(
			"api/admin/system/time",
			{
				method: 'POST',
				body: JSON.stringify(payload),
				headers: new Headers({'content-type': 'application/json'})
			}
		)
	},
	applyWifi: ()=>{
		payload = {
			mode: $('input[name=wifiMode]:checked', '#frmWifiSettings').val(),
			client: {
				ssid: $("#clientSSID").val(),
				passphrase: $("#clientPASS").val()
			},
			hotspot: {
				ssid: $("#hotspotSSID").val(),
				passphrase: $("#hotspotPASS").val()
			}
		}
		fetch(
			"api/admin/system/wifi",
			{
				method: 'POST',
				body: JSON.stringify(payload),
				headers: new Headers({'content-type': 'application/json'})
			}
		)
		console.log(payload)
	}

}
