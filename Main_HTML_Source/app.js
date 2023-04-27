URL = window.URL || window.webkitURL;
const jsondata = {
	age: 0,
    education_yrs: 1,
    cigsPerDay: 0,
    glucose: 0,
    totChol: 0,
	BMI: 0,
	heartRate: 0,
	smoker: false,
    BPMeds: false,
    prevalentStroke: false,
    prevalentHyp: false,
	diabetes: false,
    sysBP: false,
    diaBP: false,
	gender: 'male',
}

function dataChange(inputname) {
	value = $(`input[name='${inputname}']`).val();
	jsondata[inputname] = value;
}

function submit() {
	// if (jsondata.age <= 0 ||
    //     jsondata.totChol <= 0 ||
    //     jsondata.cigsPerDay   <= 0 ||
    //     jsondata.glucose  <= 0 ||
    //     jsondata.totChol  <= 0 ) {
	// 		alert("age, totChol, cigsPerDay, glucose, totChol cannot be less than or equal to 0.")
	// 	return;
	// }

	console.log(jsondata)
	let formData = new FormData();
	
	const loader = $('.page-loader');
	loader.removeClass('done');
	$(".page-loader").append(`
		<div style="
		position: absolute;
		top: 40%;
		left: 50%;
		transform: translate(-50%, -50%);
		text-align: center;
		
	"><h1>AI Is Analyzing Yyour Heart Disease</h1>
	<p>It may take 10 ~ 30 seconds</p>
	</div>
	
	`);
	for (var key in jsondata) {
		formData.append(key, jsondata[key]);
	}

	var xhr = new XMLHttpRequest();
	xhr.onload = function (e) {
		console.log(this.status)
		if (this.status == 200) {
			result = JSON.parse(e.target.responseText);
			message = result.message;
			$(".page-loader").empty();
		 	$("#content").empty();
		 	$("#content").append(`
		 	<div
		 	class=""
		 	style="height: 85vh; position: relative; "
		 	>
		 		<div
		 		style="
		 			margin: 0;
		 			position: absolute;
		 			top: 50%;
		 			left: 50%;
		 			transform: translate(-50%, -50%);
		 			text-align: center;
		 		"
		 		>
		 	  <h1>${message}</h1>
		 	  <p>Our recommended online clinic - <a href="https://www.doctoroncall.com.my/">DoctorOnCall</a></p>
		 	  <a href="/" class="btn btn-primary">Go Back Home</a>
		 	</div>
		 	 </div>
		 	`)
		 }
		if (this.status == 400) {
			alert("Server returned: ", e.target.responseText);
		}
		if (this.status == 500) {
			alert("Server error: 500, try again or contact 010-9361029 for help");
		}
		loader.addClass('done');
	};
	// xhr.open("POST", "https://api.imjordan.me/predict", true);
	xhr.open("POST", "http://localhost:8000/predict", true);
	xhr.send(formData);
}
