#Switch Directory to UsageTracker
cd UsageTracker

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

#install reqs
pip install -r requirements.txt

# Apply database migrations
python manage.py makemigrations
python manage.py migrate

# Load initial data
python manage.py loaddata customer_data.json
python manage.py loaddata usage_data.json

#runserver

python manage.py runserver