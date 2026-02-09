# API/Payloads/member_payload.py

import random
import string


class MemberPayload:

    @staticmethod
    def generate_member_id():
        """
        Generates unique member ID
        to avoid duplicate member creation
        """
        return "AUTO_" + ''.join(random.choices(string.digits, k=5))

    @staticmethod
    def create_member_payload():
        """
        Returns payload for
        Create Member API
        """

        member_id = MemberPayload.generate_member_id()

        payload = {

            # Unique member identifier
            "member_id": member_id,

            # Basic profile details
            "first_name": "test_first_name",
            "last_name": "test_last_name",
            "member_status": "active",

            # Email with unique member ID
            "email_address": f"test+{member_id}@gmail.com",
            "email_subscription_status": "subscribed",

            # Contact info
            "phone_number": "+101-12234567890",

            # Date fields (MM/DD format)
            "birthdate": "09/13",
            "anniversary_date": "09/10/2025",

            # Referral info
            "referrer_code": "WAL1E842",

            # Tags assigned to member
            "member_tags": [
                "recurring"
            ],

            # Address object (Nested JSON)
            "address": {
                "city": "PUNE",
                "country": "India",
                "line2": "MG Road",
                "line1": "Pune Street",
                "state": "Maharashtra",
                "postal_code": "411001"
            },

            # Custom attributes (Optional)
            "custom_attributes": {}
        }

        return payload
