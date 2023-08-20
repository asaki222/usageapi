import requests
from usage_client.exceptions import ValidationError, NetworkError

class UsageAPIClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def create_usage(self, customer_id):
        url = f"{self.base_url}/api/v1/usage/create/"
        data = {"customer_id": customer_id } 

        if not data.get("customer_id"):
            raise ValidationError("customer", "Customer cannot be empty")

        try:
            response = requests.post(url, json=data)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            raise NetworkError(str(e))