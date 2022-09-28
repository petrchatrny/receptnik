let lastSearch = {"format": "html", "page": 1};
let recipes = "";
let filtersOpened = false;

$(document).ready(() => {
    fetchRecipes(lastSearch, true);
    updateMaxPreparationTime()
});

function fetchRecipes(jsonData, replace) {
    lastSearch = jsonData;

    $.ajax({
        type: "GET",
        url: getRootUrl() + "/api/recipes/",
        data: jsonData,
        success: (res) => {
            // process data from server
            if (replace) {
                recipes = res["data"]
            } else {
                recipes += res["data"]

                // hide loading
                changeLoadingItemVisibility("#loading-animation", false);
            }

            // update recipes
            $("#recipes").html(recipes);

            // hide load-more-button if it should be hidden
            if (res["page"] >= res["max_page"] || res["max_page"] === 0) {
                changeLoadingItemVisibility("#load-more-button", false);
            } else {
                changeLoadingItemVisibility("#load-more-button", true);
            }
        },
        error: (res) => {
            // hide loading
            changeLoadingItemVisibility("#loading-animation", false);
            alert(res);
        }
    });
}

function submitSearch(e) {
    // prevent page reload
    e.preventDefault();

    // scrape data from form
    let jsonData = Object.fromEntries(new FormData(e.target).entries());
    jsonData["format"] = "html";
    jsonData["page"] = 1;

    // get recipes from API using form data
    fetchRecipes(jsonData, true);
}

function loadMore() {
    // show loading
    changeLoadingItemVisibility("#load-more-button", false);
    changeLoadingItemVisibility("#loading-animation", true);

    // update data
    let jsonData = lastSearch;
    jsonData["page"] = jsonData["page"] + 1;
    fetchRecipes(jsonData, false);
}

function changeLoadingItemVisibility(item, visible) {
    if (visible) {
        $(item).css("display", "flex");
    } else {
        $(item).css("display", "none");
    }
}

function changeFiltersVisibility() {
    let filters = $("#filters");
    if (filtersOpened) {
        filters.fadeOut("slow");
        filtersOpened = false;
    } else {
        filters
            .css("display", "flex")
            .hide()
            .fadeIn("slow");
        filtersOpened = true;
    }
}

function updateMaxPreparationTime() {
    let value = $("#max-preparation-time").val();
    let output = $("#max-preparation-time-value");
    if (value * 1 === 1) {
        output.html("1 minuta");
    } else if (value > 1 && value < 5) {
        output.html(value + " minuty");
    } else {
        output.html(value + " minut");
    }
}