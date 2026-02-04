Feature: Admin Login

  Background:
    Given the admin is on the login page

  @sanity
  Scenario: Login with valid username and password
    When the admin enters valid username and password
    Then the dashboard should be displayed

  @sanity
  Scenario: Login with invalid password
    When the admin enters invalid username or password
    Then an error message should be displayed

  @sanity
  Scenario Outline: Login with multiple invalid credentials
    When the admin enters "<username>" and "<password>"
    Then "<login_status>" should be displayed

    Examples:
    |username|password|login_status|
    |admin   |Santosh24011992#|success      |
    |admin   |wrong123|error       |