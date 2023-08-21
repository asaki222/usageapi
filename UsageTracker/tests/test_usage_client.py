import unittest
from unittest.mock import Mock, patch
from usage_client import UsageAPIClient, NetworkError, ValidationError
import requests

class TestUsageAPIClient(unittest.TestCase):

    @patch("requests.post")
    def test_create_usage_successful(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 201
        mock_post.return_value = mock_response
        mock_response.json.return_value = {
            "message": "Usage entry created successfully",
        }
        client = UsageAPIClient("http://www.test.com")
        customer_id = 123

        response = client.create_usage(customer_id)
        self.assertEqual(response["message"], "Usage entry created successfully")

    @patch("requests.post")
    def test_create_usage_empty_customer(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.json.return_value = {"error": "Customer cannot be empty"}
        mock_post.return_value = mock_response

        client = UsageAPIClient("http://www.test.com")
        customer_data = ''

        with self.assertRaises(ValidationError) as context:
            client.create_usage(customer_data)

        self.assertEqual(str(context.exception), '{"error": "Customer cannot be empty", "field": "customer"}')

if __name__ == "__main__":
    unittest.main()
