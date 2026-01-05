import random
import string
from datetime import time
import random
from datetime import datetime


class DataGenerator:

    @staticmethod
    def generate_unique_text(length=5):
        """Generate a random string of letters and digits with given length."""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    @staticmethod
    def create_user():
        emp_id = random.randint(100000, 999999)  # 6-digit ID
        suffix = ''.join(random.choices(string.ascii_uppercase, k=3))

        return {
            "first_name": f"F_{suffix}",
            "middle_name": f"M_{suffix}",
            "last_name": f"L_{suffix}",
            "employee_id": str(emp_id),
            "other_id": "",
            "driver's_license_no": f"DL{emp_id}",
            "license_expiry_date": "2035-12-31",
            "gender": "Male",
            "marital_status": "Single",
            "nationality": "Indian",
            "date_of_birth": "1995-05-10",
            "address_street_1": "MG Road",
            "address_street_2": "Near Metro",
            "city": "Pune",
            "state/province": "Maharashtra",
            "zip/postal_code": "411001",
            "country": "India",
            "home_telephone": "",
            "mobile": "9999999999",
            "work_telephone": "",
            "work_email": f"email_{emp_id}@testmail.com",
            "other_email": ""
        }

    @staticmethod
    def generate_user_credentials(base_name="Admin", name="Santosh"):
        """
        Generates a unique username and password.

        Username: base_name + name + date + random number (optional)
        Password: name + date + special character #

        Example:
            Username: AdminSantosh03012026
            Password: Santosh03012026#
        """
        # Current date in DDMMYYYY format
        date_str = datetime.now().strftime("%d%m%Y")

        # Optional random 2-digit number to ensure uniqueness if needed
        rand_num = random.randint(10, 99)

        username = f"{base_name}{name}{date_str}{rand_num}"
        password = f"{name}{date_str}#"

        return username, password
