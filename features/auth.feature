Feature: Authority

  Scenario: user login
    Given : when we at user login page
    When : we input username and password
    Then : we can see application has been logged in

  Scenario: superuser login
    Given : when we at user login page
    When : we input a superuser username and password
    Then : we can see application has been logged in with a superuser


  Scenario: user logout
    Given : when we logged in with a user
    When : we click on logout link
    Then : we can see application has been logged out