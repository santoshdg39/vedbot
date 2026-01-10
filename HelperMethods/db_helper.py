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

    @staticmethod
    def get_user_status_and_role_by_username(username):
        connection = DatabaseHelper.get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT 
                u.user_name,
                u.status,
                r.name AS role_name
            FROM ohrm_user u
            JOIN ohrm_user_role r ON u.user_role_id = r.id
            WHERE u.user_name = %s
        """

        cursor.execute(query, (username,))
        result = cursor.fetchone()

        cursor.close()
        connection.close()

        if not result:
            return None
        user_data = {
            "username": result["user_name"],
            "status": "Enabled" if result["status"] == 1 else "Disabled",
            "role": "Admin" if result["role_name"].lower() == "admin" else "ESS"
        }
        return user_data
