

function sendDateTime(){
	dt = new Date()
	y = dt.getFullYear()
	m = dt.getMonth()+1
	if (m<10){
		m="0"+m
	}
	d = dt.getDate()
	if (d<10){
		d = "0" + d
	}
	h = dt.getHours()
	if (h<10){
		h="0"+h
	} 
	mi = dt.getMinutes()
	if (mi< 10){
		mi = "0" + mi
	}
	s = dt.getSeconds()
	if (s<10){
		s="0" + s
	}
	str_dt = y + "-" + m + "-" + d + "T" + h + ":" + mi + ":" + s
	data = {
		timestamp: str_dt
	}
	console.log(str_dt)
	fetch(
		"api/phone/time",
		{
			method: 'POST',
			body: JSON.stringify(data),
			headers: new Headers({'content-type': 'application/json'})
		}
	)
}
sendDateTime()