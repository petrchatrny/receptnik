function register(e) {
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

    if (jsonData.get("password") === jsonData.get("password_confirm")) {
        $.ajax({
            type: "POST",
            url: getRootUrl() + "api/users/register",
            processData: false,
            contentType: false,
            data: jsonData,
            success: (res) => {
                // empty all inputs
                $('input').val('');

                // info message
                status.css({"display": "flex", "color": "#4BB543"});
                statusIcon.html("<i class='fa-solid fa-circle-check'></i>");
                statusMessage.html("Registrace proběhla úspěšně. <br> Potvrďte ji ve svém emailu.")

                // reset button
                submitButton.html("Zaregistrovat se");
            },
            error: (res) => {
                // get response message
                let message;
                switch (res["responseJSON"]["message"]) {
                    case "missing_data":
                        message = "Nebyla vyplněny všechny údaje.";
                        break;
                    case "email_already_taken":
                        message = "Tento email je již obsazen.";
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
                submitButton.html("Zaregistrovat se");
            }
        });
    } else {
        // show error message
        status.css({"display": "flex", "color": "crimson"});
        statusIcon.html("<i class='fa-solid fa-circle-exclamation'></i>");
        statusMessage.html("Hesla se neshodují.")

        // reset button
        submitButton.html("Zaregistrovat se");
    }
}