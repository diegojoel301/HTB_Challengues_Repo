$( document ).ready(function() {
    fetchID();
    $('#sql-input').keypress(function (e) {
        if (e.which == 13) {
          execute();
          return false;
        }
      });
});


const fetchID = async() => {
    let debug_pass = $('#debug-pass').val();

    await fetch(`/debug/sql/exec`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({sql: 'select * from enrollments', password: debug_pass}),
    })
    .then((response) => response.json()
        .then((resp) => {
            if (response.status == 200) {
                $(".sql-sqlstr").text(`$ ${resp.sql}`);
                $(".sql-output").text(resp.output);
            }
            else {
                $(".sql-output").text(resp.message);
            }
        }))
    .catch((error) => {
        $(".sql-output").val(error.message);
    });
}

const execute = async() => {
    let debug_pass = $('#debug-pass').val();

    sql = $('#sql-input').val();

    await fetch(`/debug/sql/exec`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({sql, password: debug_pass}),
    })
    .then((response) => response.json()
        .then((resp) => {
            if (response.status == 200) {
                $(".sql-sqlstr").text(`$ ${resp.sql}`);
                $(".sql-output").text(resp.output);
            }
            else {
                $(".sql-output").text(resp.message);
            }
        }))
    .catch((error) => {
        $(".sql-output").val(error.message);
    });
}