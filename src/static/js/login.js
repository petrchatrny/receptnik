function login(e) {
    e.preventDefault();
    $(".status").css("display", "none");

    // get data
    let jsonData = new FormData(e.target);

    // show processing icon
    $(".submit-button").html("<i class='fas fa-circle-notch fa-spin'></i>");

    $.ajax({
        type: "POST",
        url: getRootUrl() + "api/users/login",
        processData: false,
        contentType: false,
        data: jsonData,
        success: () => {
            window.location.replace("/uzivatel");
        },
        error: (res) => {
            // get response message
            let message;
            switch (res["responseJSON"]["message"]) {
                case "missing_data":
                    message = "Nebyla vyplněny všechny údaje.";
                    break;
                case "wrong_credentials":
                    message = "Neplatné přihlašovací údaje.";
                    break;
                default:
                    message = "Nastala neznámá chyba.";
            }

            // show response message
            $(".status").css({"display": "flex", "color": "crimson"});
            $(".status-icon").html("<i class='fa-solid fa-circle-exclamation'></i>");
            $(".status-message").html(message)

            // reset button
            $(".submit-button").html("Přihlásit se");
        }
    });
}