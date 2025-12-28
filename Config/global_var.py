import os
import platform

if platform.system() == "windows":
    path_divider = "\\"
else:
    path_divider = "/"

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
CONFIG_PATH = os.path.join(ROOT_DIR, f"Config")
DATA_FILES_PATH = os.path.join(ROOT_DIR, f"TESTDATA")
ALLURE_RESULTS_PATH = os.path.join(ROOT_DIR, f"Report{path_divider}allureReport")
SCREENSHOT_PATH = os.path.join(ROOT_DIR, f"Artifacts{path_divider}Screenshots")
LOGS_PATH = os.path.join(ROOT_DIR, f"Artifacts{path_divider}Logs")
IMPORT_EMPLOYEE_CSV_PATH = os.path.join(ROOT_DIR, f"TESTDATA{path_divider}importData.csv")
USERS_SHEET_NAME = "Employees"
