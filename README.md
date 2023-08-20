# Usage App

This application and library allow you to efficiently track cloud usage for customers. The library simplifies the process by taking a customer ID as input and generating a bill with usage details and the total price owed for the current month. To get started, follow the steps below:

## Setting Up the API (usage_app)

The `usage_app` is a Django-based web service that handles usage data and provides an API endpoint for recording usage. To run the app locally, follow these steps:

1. Clone the repository:
   ```sh
   git clone https://github.com/your-username/usage_app.git
   cd usage_app

2. Set up a virtual environment (optional but recommended):
  `python -m venv venv
    source venv/bin/activate
    `
3. 
Create and apply database migrations:
`pip install -r requirements.txt`
4. 
Seed the database with initial data:
`python manage.py loaddata customer_data.json
      python manage.py loaddata usage_data.json
    `
5. Run development server 
``python manage.py runserver``

## Usage Client

1. Install the usage_client library:
   ``pip install git+https://github.com/your-username/usage_client.git``

2. Use it in your code
```from usage_client import UsageAPIClient, NetworkError, ValidationError

client = UsageAPIClient("http://localhost:8000")  # Adjust the URL as needed

try:
    customer_id = "324"
    response = client.create_usage(customer_id)
    print(f"Response: {response.status_code}")
except ValidationError as e:
    print(f"Validation Error: {e}")
except NetworkError as e:
    print(f"Network Error: {e}")

```