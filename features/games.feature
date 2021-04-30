Feature: searching

    Scenario: search a game
        Given we want to find a game
        When we fill in the name of the into search bar
        Then show the search result

    Scenario: check game details
        Given we are at a game list page
        When we click on one of the game name
        Then we will be redirect to game detail