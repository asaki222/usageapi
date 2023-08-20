from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import AccumulatedUsage, Customer, Usage
from django.utils import timezone

class AccumulatedUsageAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.customer = Customer.objects.create(name='Test Customer')
        Usage.objects.create(
            customer= self.customer,
            service='Load Balancer',
            units_consumed=27,
            price_per_unit='20.00',
            usage_date=timezone.now().date()  
        )# Make sure to use the date, not datetime
    

    def test_create_accumulated_usage(self):
        response = self.client.post('/api/v1/usage/create/', {"customer":self.customer.pk})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_duplicate_accumulated_usage(self):
        self.client.post('/api/v1/usage/create/',  {"customer":self.customer.pk})
        response = self.client.post('/api/v1/usage/create/', {"customer":self.customer.pk})
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def tearDown(self):
        # Clean up any test data or resources
        AccumulatedUsage.objects.all().delete()
        Customer.objects.all().delete()
