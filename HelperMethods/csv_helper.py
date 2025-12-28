import csv
import os


class CSVHelper:
    headers = [
        "first_name", "middle_name", "last_name", "employee_id",
        "other_id", "driver's_license_no", "license_expiry_date",
        "gender", "marital_status", "nationality", "date_of_birth",
        "address_street_1", "address_street_2", "city", "state/province",
        "zip/postal_code", "country", "home_telephone", "mobile",
        "work_telephone", "work_email", "other_email"
    ]

    @staticmethod
    def clear_and_create(file_path):
        with open(file_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(CSVHelper.headers)

    @staticmethod
    def add_rows(file_path, data):
        with open(file_path, "a", newline="", encoding="utf-8") as f:
            # with open(...) as f: This will.....
            # Automatically open the file
            # Automatically closes the file when done
            # Handles exceptions safely

            writer = csv.writer(f)
            # csv.writer() is a function from Python’s built-in csv module.
            # Create a CSV writer object that knows how to write rows into the file f.
            # It provides methods like:
            # writer.writerow(...)
            # writer.writerows(...)

            for row in data:
                if isinstance(row, dict):
                    # isinstance(row, dict) checks whether the current data row is a dictionary. If it is, the code
                    # converts it into an ordered list before writing to CSV, because CSV files require ordered values.

                    row_list = [
                        row.get("first_name", ""),
                        row.get("middle_name", ""),
                        row.get("last_name", ""),
                        row.get("employee_id", ""),
                        row.get("other_id", ""),
                        row.get("driver's_license_no", ""),
                        row.get("license_expiry_date", ""),
                        row.get("gender", ""),
                        row.get("marital_status", ""),
                        row.get("nationality", ""),
                        row.get("date_of_birth", ""),
                        row.get("address_street_1", ""),
                        row.get("address_street_2", ""),
                        row.get("city", ""),
                        row.get("state/province", ""),
                        row.get("zip/postal_code", ""),
                        row.get("country", ""),
                        row.get("home_telephone", ""),
                        row.get("mobile", ""),
                        row.get("work_telephone", ""),
                        row.get("work_email", ""),
                        row.get("other_email", "")
                    ]
                    writer.writerow(row_list)
                else:
                    # Handles rows provided as list/tuple (not dictionary).
                    # Ensures the number of values in the row matches CSV headers

                    if len(row) != len(CSVHelper.headers):
                        raise ValueError(
                            f"Row length mismatch: expected {len(CSVHelper.headers)}, got {len(row)}"
                        )
                    writer.writerow(row)

    @staticmethod
    def read_rows(file_path):
        rows = []
        with open(file_path, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(row)
        return rows
