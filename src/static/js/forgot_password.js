function resetPassword(e) {
    e.preventDefault();

    let status = $(".status");
    let submitButton = $(".submit-button");
    let statusIcon = $(".status-icon");
    let statusMessage = $(".status-message")

    status.css("display", "none");

    // show processing icon
    submitButton.html("<i class='fas fa-circle-notch fa-spin'></i>");

    // get data
    let jsonData = new FormData(e.target);

    $.ajax({
        type: "POST",
        url: getRootUrl() + "api/users/forgot-password",
        processData: false,
        contentType: false,
        data: jsonData,
        success: (res) => {
            // empty all inputs
            $('input').val('');

            // info message
            status.css({"display": "flex", "color": "#4BB543"});
            statusIcon.html("<i class='fa-solid fa-circle-check'></i>");
            statusMessage.html("Žádost byla úspěšně odeslána")

            // reset button
            submitButton.html("Obnovit heslo");
        },
        error: (res) => {
            // get response message
            let message;
            switch (res["responseJSON"]["message"]) {
                case "missing_data":
                    message = "Nebyla vyplněny všechny údaje.";
                    break;
                case "invalid_email":
                    message = "Neplatná emailová adresa.";
                    break;
                default:
                    message = "Nastala neznámá chyba.";
            }

            // show response message
            status.css({"display": "flex", "color": "crimson"});
            statusIcon.html("<i class='fa-solid fa-circle-exclamation'></i>");
            statusMessage.html(message)

            // reset button
            submitButton.html("Obnovit heslo");
        }
    });
}

function newPassword(e) {
    e.preventDefault();

    let status = $(".status");
    let submitButton = $(".submit-button");
    let statusIcon = $(".status-icon");
    let statusMessage = $(".status-message")

    status.css("display", "none");

    // show processing icon
    submitButton.html("<i class='fas fa-circle-notch fa-spin'></i>");

    // get data
    let jsonData = new FormData(e.target);

    $.ajax({
        type: "POST",
        url: getRootUrl() + `api/users/update-password/${jsonData.get('code')}`,
        processData: false,
        contentType: false,
        data: jsonData,
        success: (res) => {
            // empty all inputs
            $('input').val('');

            // info message
            status.css({"display": "flex", "color": "#4BB543"});
            statusIcon.html("<i class='fa-solid fa-circle-check'></i>");
            statusMessage.html("Heslo bylo úspěšně změněno. Budete přesměrováni.")

            // reset button
            submitButton.html("Nastavit heslo");
            setTimeout(() => {
                changePage(getRootUrl() + '/prihlaseni')
            }, 2000);

        },
        error: (res) => {
            // get response message
            let message;
            switch (res["responseJSON"]["message"]) {
                case "missing_data":
                    message = "Nebyla vyplněny všechny údaje.";
                    break;
                case "invalid_link":
                    message = "Poškozený odkaz.";
                    break;
                case "link_expired":
                    message = "Platnost odkazu již vypršel.";
                    break;
                case "link_already_used":
                    message = "Odkaz byl již využit.";
                    break;
                default:
                    message = "Nastala neznámá chyba.";
            }

            // show response message
            status.css({"display": "flex", "color": "crimson"});
            statusIcon.html("<i class='fa-solid fa-circle-exclamation'></i>");
            statusMessage.html(message)

            // reset button
            submitButton.html("Nastavit heslo");
        }
    });
}