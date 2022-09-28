let ingredientCounter = 1;
let stepCounter = 1;
const INGREDIENT_LIMIT = 20;
const STEP_LIMIT = 15;

function showThumbnail(input) {
    if (input.files && input.files[0]) {
        let reader = new FileReader();

        reader.onload = (e) => {
            $("#thumbnail").attr("src", e.target.result).width(150).height(200);
        };
        reader.readAsDataURL(input.files[0]);
    }
}

function addIngredient() {
    if (ingredientCounter !== INGREDIENT_LIMIT) {
        ingredientCounter++;

        let ingredient = `<div class="ingredient" id="ingredient-${ingredientCounter}">
                <label>
                    Název
                    <input onkeyup="autocompleteIngredient(event)" type="text" name="ingredient_name-${ingredientCounter}" required>
                </label>
                <label>
                    Množství
                    <input type="number" min="1" class="short" name="ingredient_value-${ingredientCounter}" required>
                </label>
                <label>
                    Veličina
                    <input type="text" class="short" name="ingredient_unit-${ingredientCounter}" required>
                </label>
            </div>`

        $("#ingredients").append(ingredient)
    }
}

function removeIngredient() {
    if (ingredientCounter !== 1) {
        $(`#ingredient-${ingredientCounter}`).remove()
        ingredientCounter--;
    }
}

function addStep() {
    if (stepCounter !== STEP_LIMIT) {
        stepCounter++;
        $("#steps").append(`<li id="step-${stepCounter}"><input type="text" name="step-${stepCounter}" required></li>`)
    }
}

function removeStep() {
    if (stepCounter !== 1) {
        $(`#step-${stepCounter}`).remove()
        stepCounter--;
    }
}

function submitRecipeCreation(e) {
    e.preventDefault();

    let submitButton = $("#create-recipe-button");
    let errorMessage = $("#error-message");

    submitButton.prop("disabled", true);
    submitButton.html("<i class='fas fa-circle-notch fa-spin'></i>");
    errorMessage.html("");

    // extract raw data
    let formData = new FormData(e.target);

    // send request to API
    $.ajax({
        type: "POST",
        url: getRootUrl() + "api/recipes/",
        processData: false,
        contentType: false,
        data: formData,
        success: (res) => {
            errorMessage.html("Recept úspěšně vytvořen. Budete přesměrováni.");
            window.location.href = getRootUrl() + `/recepty/${res.recipe_id}`;
        },
        error: (res) => {
            submitButton.prop("disabled", false);
            submitButton.html("Vytvořit recept");
            let rip = "Recept nebyl vytvořen - ";
            switch (res.responseJSON.message) {
                case "wrong_data_format":
                    errorMessage.html(rip + "Data nejsou ve správném formátu.");
                    break;
                case "missing_data":
                    errorMessage.html(rip + "Nebyla vyplněna nezbytná data.");
                    break;
                case "too_many_ingredients":
                    errorMessage.html(rip + "Bylo zadáno příliš mnoho ingrediencí.");
                    break;
                case "wrong_image_format":
                    errorMessage.html(rip + "Obrázek nemá správný formát. Povolené formáty jsou: jpg, png, gif.");
                    break;
                default:
                    errorMessage.html(rip + "Nastala neznámá chyba.");
            }
        }
    });
}

function autocompleteIngredient(e) {
    let value = e.target.value;
    if (value === "") {
        return;
    }
    $.ajax({
        type: "GET",
        url: getRootUrl() + `/api/ingredients?name=${value}`,
        success: (res) => {
            // parse result
            let ingredients = res.map((ingredient) => {
                return ingredient["name"]
            })

            // autocomplete
            $(`[name=${e.target.name}]`).autocomplete({
                source: ingredients
            });
        }
    });
}