if (getCookie("showKeyDeleteSnack") === "") {
    setCookie("showKeyDeleteSnack", false);
}

if (getCookie("showRecipeDeleteSnack") === "") {
    setCookie("showRecipeDeleteSnack", false);
}

if (getCookie("showKeyCreatedSnack") === "") {
    setCookie("showKeyCreatedSnack", false);
}

$(document).ready(() => {
    if (getCookie("showKeyDeleteSnack") === "true") {
        openTab("keys");
        showSnackBar("Klíč byl smazán");
        setCookie("showKeyDeleteSnack", false);
    } else if (getCookie("showKeyCreatedSnack") === "true") {
        openTab("keys");
        showSnackBar("Klíč byl vytvořen");
        setCookie("showKeyCreatedSnack", false);
    } else if (getCookie("showRecipeDeleteSnack") === "true") {
        openTab("recipes");
        showSnackBar("Recept byl smazán");
        setCookie("showRecipeDeleteSnack", false);
    } else {
        openTab("recipes");
    }
});

function openTab(tabName) {
    switch (tabName) {
        case "recipes":
            document.getElementById("keys-table").style.display = "none";
            document.getElementById("recipes-table").style.display = "table";
            document.getElementById("keys-tab").classList.remove("active-tab");
            document.getElementById("recipes-tab").classList.add("active-tab");
            //document.getElementById("recipes-error-message").style.display = "block";
            break;
        case "keys":
            document.getElementById("keys-table").style.display = "table";
            document.getElementById("recipes-table").style.display = "none";
            document.getElementById("keys-tab").classList.add("active-tab");
            document.getElementById("recipes-tab").classList.remove("active-tab");
            //document.getElementById("keys-error-message").style.display = "none";
            break;
    }
}

function copyKeyToClipboard(e) {
    navigator.clipboard.writeText(e.target.innerHTML);
    showSnackBar("Klíč uložen do schránky (použijte CTRL + V).");
}

function changeApiKeyActivation(e, key_id) {
    $.ajax({
        type: "POST", url: getRootUrl() + `api/api-keys/${key_id}/activation`, success: (res) => {
            e.target.checked = res["is_key_active"];
        }, error: (res) => {
            e.target.checked = !e.target.checked;
            switch (res.status) {
                case 401:
                    showSnackBar("Chyba: vaše přihlášení vypršelo!");
                    break;
                case 403:
                    showSnackBar("Chyba: snažíte se měnit cizí klíč.");
                    break;
                default:
                    showSnackBar("Nastala neznámá chyba.");
            }
        }
    });
}

function deleteUser(e, user_id) {
    $.ajax({
        type: "DELETE",
        url: getRootUrl() + `api/users/${user_id}`,
        success: (res) => {
            changePage(getRootUrl() + "rozlouceni");
        },
        error: (res) => {
            switch (res.status) {
                case 401:
                    showSnackBar("Chyba: vaše přihlášení vypršelo!");
                    break;
                case 403:
                case 404:
                    showSnackBar("Chyba: Nelze smazat tohoto uživatele!");
                    break;
                default:
                    showSnackBar("Nastala neznámá chyba.");
            }
        }
    });
}

function deleteApiKey(e, key_id) {
    $.ajax({
        type: "DELETE",
        url: getRootUrl() + `api/api-keys/${key_id}`,
        success: (res) => {
            setCookie("showKeyDeleteSnack", true)
            location.reload();
        },
        error: (res) => {
            switch (res.status) {
                case 401:
                    showSnackBar("Chyba: vaše přihlášení vypršelo!");
                    break;
                case 403:
                    showSnackBar("Chyba: snažíte se měnit cizí klíč.");
                    break;
                default:
                    showSnackBar("Nastala neznámá chyba.");
            }
        }
    });
}

function deleteRecipe(e, recipe_id) {
    $.ajax({
        type: "DELETE", url: getRootUrl() + `api/recipes/${recipe_id}`, success: (res) => {
            setCookie("showRecipeDeleteSnack", true)
            location.reload();
        }, error: (res) => {
            switch (res.status) {
                case 401:
                    showSnackBar("Chyba: vaše přihlášení vypršelo!");
                    break;
                case 403:
                    showSnackBar("Chyba: snažíte se měnit cizí klíč.");
                    break;
                default:
                    showSnackBar("Nastala neznámá chyba.");
            }
        }
    });
}

function showDeleteKeyDialog(e, key_id) {
    setupConfirmDialog("Smazání klíče", "Opravdu chcete smazat svůj API klíč? Tento krok nelze vzít zpět.", () => {
        deleteApiKey(e, key_id);
    });
    openConfirmDialog();
}

function showDeleteRecipeDialog(e, recipe_id) {
    setupConfirmDialog("Smazání receptu", "Opravdu chcete smazat svůj recept? Tento krok nelze vzít zpět.", () => {
        deleteRecipe(e, recipe_id);
    });
    openConfirmDialog();
}

function showDeleteUserDialog(e, user_id) {
    setupConfirmDialog("Smazání účtu", "Opravdu chcete smazat svůj účet? Smažete tím také všechny své recepty. Tento krok nelze vzít zpět.", () => {
        deleteUser(e, user_id);
    });
    openConfirmDialog();
}