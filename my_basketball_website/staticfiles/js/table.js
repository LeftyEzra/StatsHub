
if (typeof jQuery !== 'undefined') {
    console.log('jQuery is loaded!');
} else {
    console.log('jQuery is NOT loaded!');
}

$(document).ready(function() {
    console.log("Document is ready!");
    $("#toggle-button").click(function() {
        console.log("Button clicked!");
        $("#description_list").toggle();
    });