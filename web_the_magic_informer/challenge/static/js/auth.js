$(document).ready(function() {
	$("#login-btn").on('click', () => { auth('login') });
    $("#register-btn").on('click', () => { auth('register') });
});

function toggleInputs(state) {
	$("#username").prop("disabled", state);
	$("#password").prop("disabled", state);
	$("#login-btn").prop("disabled", state);
	$("#register-btn").prop("disabled", state);
}

const auth = async (intent) => {

	toggleInputs(true);

	// prepare alert
	let card = $("#resp-msg");
	card.attr("class", "alert alert-info");
	card.hide();

	let user = $("#username").val();
	let pass = $("#password").val();

	if ($.trim(user) === '' || $.trim(pass) === '') {
		toggleInputs(false);
		card.text("Please input username and password first!");
		card.attr("class", "alert alert-danger");
		card.show();
		return;
	}

	await fetch(`/api/${intent}`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify({
                username: user,
                password: pass
            }),
		})
		.then((response) => response.json()
			.then((resp) => {
				if (response.status == 200) {
					card.text(resp.message);
					card.attr("class", "alert alert-success");
					card.show();
                    setTimeout(() => {
                        if (intent == 'login') {
                            window.location.href = '/dashboard';
                        }
                        else {
                            window.location.href = '/login';
                        }
                    }, 1000);
				}
				card.text(resp.message);
				card.attr("class", "alert alert-danger");
				card.show();
			}))
		.catch((error) => {
			card.text(error);
			card.attr("class", "alert alert-danger");
			card.show();
		});

	toggleInputs(false);
}