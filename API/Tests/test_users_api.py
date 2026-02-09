from API.Clients.api_client import APIClient
from API.Payloads.user_payloads import MemberPayload
from API.Endpoints.user_endpoints import UserEndpoints


class TestCreateMember:

    def setup_method(self):
        self.client = APIClient()

    def test_create_member(self):

        payload = MemberPayload.create_member_payload()

        response = self.client.post(
            endpoint=UserEndpoints.CREATE_MEMBER,
            payload=payload
        )

        print(response.json())

        assert response.status_code in [200, 201]

    def test_create_member_success_flag(api_client, member_payload):
        response = api_client.post(
            endpoint="/v2/loyalty/members",
            payload=member_payload
        )

        response_json = response.json()

        assert response_json["success"] is True

    def test_member_id_created(api_client, member_payload):
        response = api_client.post(
            endpoint="/v2/loyalty/members",
            payload=member_payload
        )

        response_json = response.json()

        assert "member_id" in response_json["data"]
        assert response_json["data"]["member_id"] == member_payload["member_id"]

    def test_member_email_validation(api_client, member_payload):
        response = api_client.post(
            endpoint="/v2/loyalty/members",
            payload=member_payload
        )

        response_json = response.json()

        assert response_json["data"]["email_address"] == member_payload["email_address"]

    def test_default_points_credit(api_client, member_payload):
        response = api_client.post(
            endpoint="/v2/loyalty/members",
            payload=member_payload
        )

        data = response.json()["data"]

        assert data["available_points"] == 100
        assert data["lifetime_points_earned"] == 100

    def test_member_default_tier(api_client, member_payload):
        response = api_client.post(
            endpoint="/v2/loyalty/members",
            payload=member_payload
        )

        tier_info = response.json()["data"]["tier_info"]

        assert tier_info["loyalty_tier_name"] == "Silver"
        assert tier_info["loyalty_tier_id"] == "zrl_silver"

    def test_member_address(api_client, member_payload):
        response = api_client.post(
            endpoint="/v2/loyalty/members",
            payload=member_payload
        )

        address = response.json()["data"]["address"]

        assert address["city"] == "PUNE"
        assert address["state"] == "Maharashtra"

    def test_referral_code_generated(api_client, member_payload):
        response = api_client.post(
            endpoint="/v2/loyalty/members",
            payload=member_payload
        )

        data = response.json()["data"]

        assert data["referral_code"] is not None

    def test_member_response_schema(api_client, member_payload):
        response = api_client.post(
            endpoint="/v2/loyalty/members",
            payload=member_payload
        )

        data = response.json()["data"]

        expected_keys = [
            "member_id",
            "first_name",
            "last_name",
            "email_address",
            "available_points",
            "tier_info"
        ]

        for key in expected_keys:
            assert key in data

    def test_duplicate_member_creation(api_client, member_payload):
        # First creation
        api_client.post("/v2/loyalty/members", member_payload)

        # Duplicate creation
        response = api_client.post(
            endpoint="/v2/loyalty/members",
            payload=member_payload
        )

        assert response.status_code in [400, 409]


"""
n Member Creation API I validate:

Status code

Success flag

Member ID creation

Payload vs response data

Default loyalty points

Tier assignment

Nested fields like address

Referral code generation

Negative cases like duplicate member
"""