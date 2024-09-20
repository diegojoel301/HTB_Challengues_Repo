$(document).ready(function() {
	setDefaults();

	$("#submit-btn").on('click', addSubmission);
	$("#upload-btn").on('click', upload);

});

const setDefaults = () => {
	let gender = $("#gender_").val();
	if (gender) $("#gender_" + gender.toLowerCase()).prop("checked", true).trigger("click");
}

const addSubmission = async () => {

	$("#submit-btn").prop("disabled", true);

	// alert message
	let card = $("#resp-msg");
	card.hide();

	// input data
	const data = {
		full_name: $("#full_name").val(),
		phone: $("#phone").val(),
		birth_date: $("#birth_date").val(),
		gender: $('input[name=genderRadios]:checked').val(),
		biography: $("#biography").val(),
	};

	await fetch('/api/enroll', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify(data),
		})
		.then((response) => response.json()
			.then((resp) => {
				if (response.status == 200) {
					card.text(resp.message);
					card.show();
                    $("#submit-btn").prop("disabled", false);
					return;
				}
				card.text(resp.message);
				card.show();
			}))
		.catch((error) => {
			card.text(error);
			card.show();
		});

	$("#submit-btn").prop("disabled", false);
}


const upload = async () => {

	$("#upload-btn").prop("disabled", true);

	let card = $("#resp-msg2");
	card.text('Please wait...');
	card.show();

	if ($('input[type=file]')[0].files.length == 0) {
		card.text('Please select a file to upload!');
		$("#upload-btn").prop("disabled", false);
		return;
	}

	let resumeFile = $('input[type=file]')[0].files[0];
	let formData = new FormData();
	formData.append('resumeFile', resumeFile);

	await fetch('/api/upload', {
			method: 'POST',
			credentials: 'include',
			body: formData,
		})
		.then((response) => response.json()
			.then((resp) => {
				if (response.status == 200) {
					$('#uploaded-file-ref').attr('class','');
					$('#uploaded-file').attr('href',`/download?resume=${resp.filename}`);
					$('#uploaded-file').text(resp.filename);
					card.attr("class", "alert alert-success");
				}
				resumeFile.value = [];
				$('#file-label').text("No file selected.");
				card.text(resp.message);
			}))
		.catch((error) => {
			card.text("This file could not be uploaded, please try again!");
		});

	$("#upload-btn").prop("disabled", false);
}