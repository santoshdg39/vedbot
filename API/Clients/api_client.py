import requests
from HelperMethods.config_parser import ReadProp


class APIClient:

    def __init__(self):
        """
        Reads API configuration from api_config.ini
        Uses existing ReadProp utility
        """

        # Read Base URL
        self.base_url = ReadProp.get_config_data(
            ini_file="api_config.ini",
            section="BASE",
            key="base_url"
        )

        # Read Authentication Details
        self.api_key = ReadProp.get_config_data(
            ini_file="api_config.ini",
            section="AUTH",
            key="api_key"
        )

        self.partner_id = ReadProp.get_config_data(
            ini_file="api_config.ini",
            section="AUTH",
            key="partner_id"
        )

        # Default Headers (as per Zinrelo requirement style)
        self.headers = {
            "Content-Type": "application/json",
            "api-key": self.api_key,
            "partner-id": self.partner_id
        }

    # -------------------- POST --------------------
    def post(self, endpoint, payload, headers=None):
        """
        Send POST request
        """
        final_headers = headers if headers else self.headers

        return requests.post(
            url=self.base_url + endpoint,
            json=payload,
            headers=final_headers
        )

    # -------------------- GET --------------------
    def get(self, endpoint, headers=None):
        """
        Send GET request
        """
        final_headers = headers if headers else self.headers

        return requests.get(
            url=self.base_url + endpoint,
            headers=final_headers
        )

    # -------------------- PUT --------------------
    def put(self, endpoint, payload, headers=None):
        """
        Send PUT request
        """
        final_headers = headers if headers else self.headers

        return requests.put(
            url=self.base_url + endpoint,
            json=payload,
            headers=final_headers
        )

    # -------------------- DELETE --------------------
    def delete(self, endpoint, headers=None):
        """
        Send DELETE request
        """
        final_headers = headers if headers else self.headers

        return requests.delete(
            url=self.base_url + endpoint,
            headers=final_headers
        )
