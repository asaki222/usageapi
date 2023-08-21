import requests
from usage_client.exceptions import NetworkError, ValidationError
from builtins import isinstance

class UsageAPIClient:
    def __init__(self, base_url):
        self.base_url = base_url
           
    def create_usage(self, customer_id):
        url = f"{self.base_url}/api/v1/usage/create/"
        data = {"customer": customer_id}

        if not data.get("customer"):
            raise ValidationError("customer", "Customer cannot be empty")

        try:
            response = requests.post(url, data)
            return response.json() 
        except requests.exceptions.RequestException as e:
            if isinstance(e, requests.exceptions.HTTPError):
                status_code = e.response.status_code
                raise NetworkError("Network Error", status_code=status_code)
            else:
                raise NetworkError("Network Error", status_code=status_code)