# Usage App

This application and library allow you to efficiently track cloud usage for customers. The library simplifies the process by taking a customer ID as input and generating a bill with usage details and the total price owed for the current month. First here's some links to navigate this README:

### Table Of Contents
1. [Setting Up the API (usage_app)](#setting-up-the-api-usage_app-manually)
2. [Usage Client](#usage-client)
3. [Running Tests](#running-tests)

## Setting Up the API (usage_app) 

The `usage_app` is a Django-based web service that handles usage data and provides an API endpoint for recording usage. To run the app locally:

Use this bash script

   Run this bash script
   ```
   chmod +x setup_script.sh
   ./setup_script.sh
   ```

OR run this manually

1. Clone the repository:
  ```
   git clone https://github.com/your-username/usage_app.git
   cd UsageTracker
  ```

2. Set up a virtual environment (optional but recommended):
  ```
    python3 -m venv venv
    source venv/bin/activate
  ```

3. Create and apply database migrations:
   ```
      pip install -r requirements.txt
   ```

4. Seed the database with initial data:

   ```
      python manage.py makemigrations 
      python manage.py migrate
      python manage.py loaddata customer_data.json
      python manage.py loaddata usage_data.json
   ```

5. Run development server 
   ```
      python manage.py runserver
   ```

## Usage Client

The usage client takes in the id of a customer. When we use the method, it fires a post request that will add to that customer's current bill based on their usage.

1. Install the usage_client library (make sure you are still in the virtualenv or changed it if you are running it):
   ``pip install .`

2. To test, open up your terminal and launch a python:

#### This client currently only accepts integers as customer ids

```
python3
```

```
from usage_client import UsageAPIClient

client = UsageAPIClient("http://localhost:8000")  # Adjust the URL as needed
client.create_usage(123)

```

### Expected Behavior of Usage Client

### No new usage data found for customer or bill for customer

``
{'message': {'message': 'No accumulated usage record or usage records found for customer Alice.'}}
``

### Posting to get a new recording of usage should give you this result

``
{'message': {'id': 1, 'month': 8, 'year': 2023, 'accumulated_price': '16.61', 'price_in_dollars': '$16.61', 'customer': 456}}
``

### If there was already a record it should give you this id

``
{'message': {'message': 'Entry has already been processed for customer Bob.', 'data': {'total_price': '$16.61'}}}
``

### If no record exist

``
{'message': 'No accumulated usage record or usage records found for customer.'}
``

## Running Tests

```
python manage.py test usage_app.test_usage_app

python manage.py test tests.test_usage_client
```