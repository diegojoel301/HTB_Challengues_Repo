$( document ).ready(function() {
    $('#sendTestBtn').on('click', testSMS);
    $('#saveBtn').on('click', saveSMS);
});


const testSMS = async () => {

    const options = {
        verb: $('#sms-verb').val(),
        url: $('#sms-url').val(),
        params: $('#sms-params').val(),
        headers: $('#sms-headers').val(),
        resp_ok: $('#sms-success-resp').val(),
        resp_bad: $('#sms-fail-resp').val(),
    }

    await fetch(`/api/sms/test`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(options),
    })
    .then((response) => response.json()
        .then((resp) => {
            if (resp.hasOwnProperty('message')) {
                $('#respModalMsg').val(resp.message);
            }
            else {
                $('#respModalMsg').val(resp.result);
            }
            new bootstrap.Modal('#respModal').show();
        }))
    .catch((error) => {
        $('#respModalMsg').val(error.message);
        new bootstrap.Modal('#respModal').show();
    });
}

const saveSMS = async() => {


    const options = {
        verb: $('#sms-verb').val(),
        url: $('#sms-url').val(),
        params: $('#sms-params').val(),
        headers: $('#sms-headers').val(),
        resp_ok: $('#sms-success-resp').val(),
        resp_bad: $('#sms-fail-resp').val(),
    }

    await fetch(`/api/sms/save`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(options),
    })
    .then((response) => response.json()
        .then((resp) => {
            $('#respConfModalMsg').text(resp.message);
            new bootstrap.Modal('#respConfModal').show();
        }))
    .catch((error) => {
        $('#respConfModalMsg').val(error.message);
        new bootstrap.Modal('#respConfModal').show();
    });
}