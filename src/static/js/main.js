function changePage(page) {
    window.location.href = page;
}

function getRootUrl() {
    let url = window.location;
    return url.protocol + "//" + url.host + "/";
}

function getCookie(name) {
    let value = `; ${document.cookie}`;
    let parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

function setCookie(name, value) {
    document.cookie = `${name}=${value};`;
}

function showSnackBar(text) {
    let snackbar = $("#snackbar");
    snackbar.html(text);
    snackbar.addClass("show");
    setTimeout(() => {
        snackbar.removeClass("show");
    }, 3000);
}

function setupConfirmDialog(title, text, result) {
    $("#confirm-dialog-title").html(title);
    $("#confirm-dialog-text").html(text);
    $("#confirm-dialog-accept").click(result);
}

function openConfirmDialog() {
    $("#confirm-dialog").css("display", "flex");
}

function closeConfirmDialog() {
    $("#confirm-dialog").hide();
}