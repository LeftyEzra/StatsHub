
 $(document).ready(function(){
        console.log('Document is ready');

        // Function to reset tables to default state
        function resetTables() {
            $(".table-wrapper").not(':first').hide(); // Hide all tables except the first one
            $(".table-wrapper:first").show(); // Ensure the first table is visible
        }

        // Attach a click event handler to all nav links
        $(".nav-link").click(function(event) {
            event.preventDefault(); // Prevent the default action of the anchor tag (page reload)
            console.log('Nav link clicked');

            // Remove 'active' class from all nav links
            $(".nav-link").removeClass("active");

            // Add 'active' class to the clicked nav link
            $(this).addClass("active");

            // Check if the clicked link is the "Games" link
            if ($(this).attr('id') === 'games') {
                console.log('Games link clicked');
                // Toggle visibility of all table-wrapper elements except the first one
                $(".table-wrapper").not(':first').fadeToggle();

            } else {
                // Reset tables to default state when any other link is clicked
                resetTables();
                console.log($(this).text() + ' link clicked');
                // Allow default action for other links by navigating to the URL
                window.location.href = $(this).attr('href');


            }
        });
 });
