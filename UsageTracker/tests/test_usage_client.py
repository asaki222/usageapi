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

        client = UsageAPIClient("http://www.test.com")
        customer_id =123

        response = client.create_usage(customer_id)
        self.assertEqual(response.status_code, 201)

    @patch("requests.post") 
    def test_create_usage_empty_customer(self, mock_post):
        client = UsageAPIClient("http://www.test.com")
        customer_data = ''

        with self.assertRaises(ValidationError) as context:
            client.create_usage(customer_data)

        self.assertEqual(str(context.exception), "Customer cannot be empty")

    @patch("requests.post", side_effect=requests.exceptions.RequestException("Network error"))
    def test_create_usage_network_error(self, mock_post):
        client = UsageAPIClient("http://www.test.com")
        customer_id= "123"

        with self.assertRaises(NetworkError) as context:
            client.create_usage(customer_id)

        self.assertEqual(str(context.exception), "Network error")

if __name__ == "__main__":
    unittest.main()
