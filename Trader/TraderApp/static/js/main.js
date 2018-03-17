if(!jQuery) {
    throw new Error("jQuery is required for the app to run.");
}

/* Global DOM elements. Set after init*/
var $navToggleClose;

$(document).ready(init);

function init() {
    initElements();

    initMaterialize();

    initEvents();
}

function initElements() {
    $navToggleClose = $("#nav-close");
}

function initMaterialize() {
    $("#nav-open").sideNav({
        menuWidth: "300",
        draggable: true
    });
};

function initEvents() {
    $navToggleClose.on("click", closeNavBar);
};

function closeNavBar(event) {
    event.preventDefault();
    // $(this).sideNav("hide");
    $("#sidenav-overlay").trigger("click");    
}
