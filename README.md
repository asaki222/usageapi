# Usage App

This application and library allow you to efficiently track cloud usage for customers. The library simplifies the process by taking a customer ID as input and generating a bill with usage details and the total price owed for the current month. To get started, follow the steps below:

## Setting Up the API (usage_app)

The `usage_app` is a Django-based web service that handles usage data and provides an API endpoint for recording usage. To run the app locally, follow these steps:

1. Clone the repository:
   ```sh
   git clone https://github.com/your-username/usage_app.git
   cd UsageTracker

2. Set up a virtual environment (optional but recommended):
  `python3 -m venv venv
    source venv/bin/activate
    `
3. 
Create and apply database migrations:
`pip install -r requirements.txt`
4. 
Seed the database with initial data:
``` 
    python manage.py migrate
    python manage.py loaddata customer_data.json
    python manage.py loaddata usage_data.json
```
5. Run development server 
``python manage.py runserver``

## Usage Client

1. Install the usage_client library:
   ``pip install .`

2. To test, open up your terminal and launch a python:

the client currently only accepts integers

``python3``

```from usage_client import UsageAPIClient

client = UsageAPIClient("http://localhost:8000")  # Adjust the URL as needed
client.create(123)

```