# steps/login_steps.py
from behave import given, when, then
from TestData import messages

@given("the admin is on the login page")
def step_impl(context):
    # Driver and page objects already initialized in environment.py
    pass

@when("the admin enters valid username and password")
def step_impl(context):
    context.loginPage.login(context.username, context.password)

@when('the admin enters "{username}" and "{password}"')
def step_impl(context, username, password):
    context.loginPage.login(username, password)

@then("the dashboard should be displayed")
def step_impl(context):
    actual_heading = context.dashboardPage.is_dashboard_displayed()
    assert messages.dashboard_page_heading_text == actual_heading, \
        f"Login failed: Dashboard not displayed. Actual: {actual_heading}"

@when("the admin enters invalid username or password")
def step_impl(context):
    context.loginPage.login(context.username, "wrongpassword")

@then("an error message should be displayed")
def step_impl(context):
    error_message = context.loginPage.get_text_value(context.loginPage.loginPageLocators.ERROR_MESSAGE)
    assert messages.invalid_password_error_message_text in error_message, \
        "Invalid credentials message is not displayed"

@then('"{login_status}" should be displayed')
def step_impl(context, login_status):
    if login_status == "success":
        actual_heading = context.dashboardPage.is_dashboard_displayed()
        assert messages.dashboard_page_heading_text == actual_heading, \
            f"Login failed: Dashboard not displayed. Actual: {actual_heading}"
    else:
        error_message = context.loginPage.get_text_value(context.loginPage.loginPageLocators.ERROR_MESSAGE)
        assert messages.invalid_password_error_message_text in error_message, \
            "Invalid credentials message is not displayed"