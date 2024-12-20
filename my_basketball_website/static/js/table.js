
$(document).ready(function() {
    console.log("Document is ready!");
    $("#toggle-button").click(function() {
        console.log("Button clicked!");
        $("#legend_container").toggle()
    });

      $("#away_toggle_button").click(function() {
        console.log("Button clicked!");

         $("#away_legend_container").toggle();
    });



});


