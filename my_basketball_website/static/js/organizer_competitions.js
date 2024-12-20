/*$(document).ready(function() {
    console.log('Document is ready');

    function resetTables() {
        $("#centerContainer, #gameFixtures, #playerSection, #table_1, #gameDates, #teamSection, #gameSummary, #gameLeaders, #singleLeaders").hide();
    }

    // Initially hide all sections
    resetTables();

    $(".nav-link").click(function(event) {
        event.preventDefault();
        console.log('Nav link clicked:', $(this).attr('id'));

        $(".nav-link").removeClass("active");
        $(this).addClass("active");

        resetTables();

        if ($(this).attr('id') === 'teamList') {
            console.log('Team List link clicked');
            $("#teamSection").fadeIn("slow");
        } else if ($(this).attr('id') === 'game_Dates') {
            console.log('Home link clicked');
            $("#gameDates").fadeIn("slow");
            $("#gameSummary").fadeIn("slow");
            $("#gameLeaders").fadeIn("slow");
            $("#singleLeaders").fadeIn("slow");
        } else if ($(this).attr('id') === 'playerList') {
            console.log('Player List link clicked');
            $("#table_1").fadeIn("slow");
        } else if ($(this).attr('id') === 'gameSchedule') {
            console.log('Game Schedule link clicked');
            $("#gameFixtures").fadeIn("slow");
            $("#centerContainer").hide();
        } else {
            console.log($(this).text() + ' link clicked');
            window.location.href = $(this).attr('href');
        }
    });

    // Show initial sections
    console.log('Initial display: showing gameDates, gameSummary, gameLeaders, singleLeaders');
    $("#gameDates").show();
    $("#gameSummary").show();
    $("#gameLeaders").show();
    $("#singleLeaders").show();
});

*/






$(document).ready(function() {
    console.log('Document is ready');

    function resetTables() {
        $("#leadersTableContainer, #standingTable, #PlayerSection, #newPlayerSection, #gameFixtures,  #gameDates, #teamSection, #gameSummary, #gameLeaders, #singleLeaders").hide();
    }

    // Initially hide all sections
    resetTables();

    $(".nav-link").click(function(event) {
        event.preventDefault();
        console.log('Nav link clicked:', $(this).attr('id'));

        $(".nav-link").removeClass("active");
        $(this).addClass("active");

        resetTables();

        if ($(this).attr('id') === 'teamList') {
            console.log('Team List link clicked');
            $("#teamSection").fadeIn("slow");
            $("#teamsSection").fadeIn("slow");

        } else if ($(this).attr('id') === 'game_Dates') {
            console.log('Home link clicked');
            $("#gameDates").fadeIn("slow");
            $("#gameSummary").fadeIn("slow");
            $("#gameLeaders").fadeIn("slow");
            $("#singleLeaders").fadeIn("slow");
            $("#newPlayerSection").hide();
            $("#teamSection").hide();
        } else if ($(this).attr('id') === 'playersList') {
            console.log('Player List link clicked');
            $("#PlayerSection").fadeIn("slow");
            $("#teamSection").hide();

        } else if ($(this).attr('id') === 'gameSchedule') {
            console.log('Game Schedule link clicked');
            $("#gameFixtures").fadeIn("slow");
            $("#newPlayerSection").hide();
            $("#teamSection").hide();

        } else if ($(this).attr('id') === 'standing') {
            console.log('Standing link clicked');
            $("#newPlayerSection").hide();
            $("#teamSection").hide();
            $("#standingTable").fadeIn("slow")


        } else if ($(this).attr('id') === 'leaders') {
            console.log('Standing link clicked');
            $("#newPlayerSection").hide();
            $("#teamSection").hide();
            $("#leadersTableContainer").fadeIn("slow")
        } else {
            console.log($(this).text() + ' link clicked');
            window.location.href = $(this).attr('href');
        }
    });

    // Initial display: hiding all sections including newPlayerSection
    resetTables();
    console.log('Initial sections hidden');
    $("#gameDates").show();
    $("#gameSummary").show();
    $("#gameLeaders").show();
    $("#singleLeaders").show();
});









$(document).ready(function() {
    console.log('Document is ready for summary');

    // Highlight the active date link
    function highlightActiveDate($element) {
        $(".card-dates").css("background-color", ""); // Reset all
        $element.css("background", "#00ff00"); // Highlight the active  linear-gradient(to top, #ffd700, #00ff00); #f06b0b
    }

    // Function to format date to 'MMM. DD, YYYY'
    function formatDate(date) {
        var options = { year: 'numeric', month: 'short', day: '2-digit' };
        var formattedDate = new Intl.DateTimeFormat('en-US', options).format(date);
        // Add a period after the month
        return formattedDate.replace(/(\w+)\s/, '$1. ');
    }

    // Get and format the current date
    var currentDate = new Date();
    var formattedCurrentDate = formatDate(currentDate);
    console.log('Formatted Current Date:', formattedCurrentDate);
    var $currentDateElement = null;

    $('.card-dates').each(function() {
        var dateText = $(this).data('date');
        console.log('Element Date:', dateText, 'Formatted Current Date:', formattedCurrentDate);
        if (dateText === formattedCurrentDate) {
            $currentDateElement = $(this);
            return false; // break out of the loop
        }
    });

    // If there is a current date element, highlight and show its games
    if ($currentDateElement) {
        console.log('Current date element found:', $currentDateElement);
        highlightActiveDate($currentDateElement); // Highlight current date
        $('.card-summary[data-date="' + $currentDateElement.data('date') + '"]').show(); // Show games for current date
    } else {
        console.log('No current date element found');
    }

    $(".card-dates").click(function(e) {
        e.preventDefault(); // Prevent default link behavior
        var $this = $(this);
        var competitionId = $this.data("competition-id");
        var date = $this.data("date");

        console.log('Date Card Clicked:', date, 'Competition ID:', competitionId);

        // Hide all card-summary elements
        $(".card-summary").hide();

        // Show the card-summary elements that match the clicked competitionId and date
        $('.card-summary[data-competition-id="' + competitionId + '"][data-date="' + date + '"]').show();

        // Highlight the active date card
        highlightActiveDate($this);
    });
});










/*
$(document).ready(function() {
    console.log('Document is ready');

    // Highlight the active date link
    function highlightActiveDate($element) {
        $(".card-dates").css("background-color", ""); // Reset all
        $element.css("background", "#00ff00");// Highlight the active  linear-gradient(to top, #ffd700, #00ff00); #f06b0b
    }

    // Function to format date to 'MMM. DD, YYYY'
    function formatDate(date) {
        var options = { year: 'numeric', month: 'short', day: '2-digit' };
        var formattedDate = new Intl.DateTimeFormat('en-US', options).format(date);
        // Add a period after the month
        return formattedDate.replace(/(\w+)\s/, '$1. ');
    }

    // Get and format the current date
    var currentDate = new Date();
    var formattedCurrentDate = formatDate(currentDate);
    // console.log('Formatted Current Date:', formattedCurrentDate);
    var $currentDateElement = null;

    $('.card-dates').each(function() {
        var dateText = $(this).data('date');
        // console.log('Element Date:', dateText, 'Formatted Current Date:', formattedCurrentDate);
        if (dateText === formattedCurrentDate) {
            $currentDateElement = $(this);
            return false; // break out of the loop
        }
    });

    // If there is a current date element, highlight and show its games
    if ($currentDateElement) {
        // console.log('Current date element found:', $currentDateElement);
        highlightActiveDate($currentDateElement); // Highlight current date
        $('.card-summary[data-date="' + $currentDateElement.data('date') + '"]').show(); // Show games for current date
    } else {
        console.log('No current date element found');
    }

    $(".card-dates").click(function(e) {
        e.preventDefault(); // Prevent default link behavior
        var $this = $(this);
        var competitionId = $this.data("competition-id");
        var date = $this.data("date");

        // console.log('Date Card Clicked:', date, 'Competition ID:', competitionId);

        // Hide all card-summary elements
        $(".card-summary").hide();

        // Show the card-summary elements that match the clicked competitionId and date
        $('.card-summary[data-competition-id="' + competitionId + '"][data-date="' + date + '"]').show();

        // Highlight the active date card
        highlightActiveDate($this);
    });
});
*/
