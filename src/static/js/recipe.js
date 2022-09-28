let rating = 0;
let ratingHTML = {};

if (getCookie("showRatingSnack") === "") {
    setCookie("showRatingSnack", false);
}

$(document).ready(() => {
    ratingHTML = $("#rating-value");
    rating = parseInt(ratingHTML.html());
    updateStars();

    if (getCookie("showRatingSnack") === "true") {
        showSnackBar("Hodnocení proběhlo úspěšně");
        setCookie("showRatingSnack", false);
    }
});

function openModal() {
    $("#rating-modal").css("display", "flex");
}

function closeModal() {
    $("#rating-modal").hide();
}

function changeRating(value) {
    if (value > 0 && rating < 5) {
        rating += value;
    } else if (value < 0 && rating > 0) {
        rating += value;
    }
    ratingHTML.html(rating);
    updateStars()
}

function updateStars() {
    for (let i = 0; i < 5; i++) {
        let star = $(`#rate-recipe-star${i}`);
        if (i < rating) {
            if (!star.hasClass("rating-star-active")) {
                star.addClass("rating-star-active");
            }
        } else {
            if (star.hasClass("rating-star-active")) {
                star.removeClass("rating-star-active");
            }
        }
    }
}

function rateRecipe(e, recipe_id) {
    e.preventDefault();

    let jsonData = new FormData();
    jsonData.append("value", rating);

    $.ajax({
        type: "POST",
        url: getRootUrl() + `api/recipes/${recipe_id}/rate`,
        processData: false,
        contentType: false,
        data: jsonData,
        success: () => {
            setCookie("showRatingSnack", true);
            location.reload();
        },
        error: (res) => {
            // get response message
            let message;
            switch (res["responseJSON"]["message"]) {
                case "unauthenticated_access":
                    message = "Vaše přihlášení vypršelo";
                    break;
                default:
                    message = "Nastala neznámá chyba na straně serveru :(";
            }

            // TODO lepší zobrazování chyb
            // show response message
            alert(message);
        }
    });
}