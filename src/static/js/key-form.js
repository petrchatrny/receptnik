function createKey(e) {
    e.preventDefault();

    let formData = new FormData(e.target);

    // send request to API
    $.ajax({
        type: "POST",
        url: getRootUrl() + "api/api-keys/",
        processData: false,
        contentType: false,
        data: formData,
        success: (res) => {
            setCookie("showKeyCreatedSnack", true);
            changePage(getRootUrl() + '/uzivatel')
        },
        error: (res) => {
            e.target.checked = !e.target.checked;
            switch (res.status) {
                case 401:
                    showSnackBar("Chyba: vaše přihlášení vypršelo!");
                    break;
                case 406:
                    showSnackBar("Chyba: máte již příliš mnoho klíčů.");
                    break;
                default:
                    showSnackBar("Nastala neznámá chyba.");
            }
        }
    });
}