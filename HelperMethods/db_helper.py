import mysql.connector
from HelperMethods.config_parser import ReadProp


class DatabaseHelper:

    @staticmethod
    def get_connection():
        return mysql.connector.connect(
            host=ReadProp.get_config_data("site_config.ini", "database", "host"),
            port=ReadProp.get_config_data("site_config.ini", "database", "port"),
            user=ReadProp.get_config_data("site_config.ini", "database", "user"),
            password=ReadProp.get_config_data("site_config.ini", "database", "password"),
            database=ReadProp.get_config_data("site_config.ini", "database", "database")
        )
    # For local OrangeHRM setup, I keep DB details under the database section in site_config.ini
    # and reuse the same config parser method to establish MySQL connections.

    @staticmethod
    def get_employee_by_id(employee_id):
        connection = DatabaseHelper.get_connection()
        curser = connection.cursor(dictionary=True)
        query = "SELECT * FROM hs_hr_employee WHERE employee_id=%s"
        curser.execute(query, (employee_id,))
        result = curser.fetchone()
        curser.close()
        connection.close()
        return result

