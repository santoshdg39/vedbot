# VedBot – Test Automation Framework

## Project Overview

**VedBot** is a Selenium–PyTest based test automation framework designed to automate web application testing using industry-standard best practices. The framework follows the **Page Object Model (POM)** design pattern to ensure scalability, maintainability, and reusability of test code.

This project demonstrates real-world automation skills such as structured test design, reusable utilities, reporting, and failure analysis.


##  Tech Stack
Programming Language:Python
Automation Tool:Selenium WebDriver
Test Framework:PyTest
Design Pattern: Page Object Model (POM)
Reporting:Allure Reports
Build / Execution: PyTest CLI
Version Control: Git & GitHub


## Folder Structure

Ved_Bot/
│
├── Config/ # Global configuration and path variables
├── Pages/ # Page Object classes
│ ├── BasePage/ # Common reusable page methods (waits, find, click)
│ └── login/ # Login page objects and locators
│
├── TestCases/ # PyTest test classes
├── TESTDATA/ # Test data files (Excel, configs)
├── Artifacts/ # Generated artifacts
│ ├── screenshots/ # Failure screenshots
│ └── Logs/ # Execution logs
│
├── Report/ # Allure report output
├── conftest.py # PyTest fixtures & hooks (driver, screenshots, reporting)
├── requirements.txt # Project dependencies
└── README.md # Project documentation


### How to Run Tests

### Install Dependencies
pip install -r requirements.txt


### Run All Tests
pytest


### Run Tests with Markers

pytest -m sanity


### Run Tests with Browser Option
pytest --browser chrome


Reports & Screenshots
Allure Report

Allure results are generated automatically after test execution.
To generate and view the report:
allure serve Report/allureReport


Screenshots on Failure
Screenshots are automatically captured when a test fails.
Stored under:
Artifacts/screenshots/
Screenshots are also attached to the Allure report for easy debugging.

Key Highlights
Page Object Model for maintainable automation
Explicit waits for stable execution
Screenshot capture on test failure
Allure integration for rich reporting
Clean and scalable project structure


Santosh Gadekar
Senior QA Engineer
GitHub: [https://github.com/santoshdg39/vedbot](https://github.com/santoshdg39/vedbot)
Test Website: https://opensource-demo.orangehrmlive.com/
