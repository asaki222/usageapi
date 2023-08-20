from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Usage(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    usage_date = models.DateTimeField()
    service = models.CharField(max_length=200)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    units_consumed = models.IntegerField()
    processed = models.BooleanField(default=False) 
    def __str__(self):
        return f"{self.customer.name} - {self.usage_date}"


class AccumulatedUsage(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    start_datetime = models.DateTimeField(blank=True, null=True)
    end_datetime = models.DateTimeField(blank=True, null=True)
    accumulated_units = models.IntegerField(blank=True, null=True)
    accumulated_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True) 
    price_in_dollars = models.CharField(max_length=10, blank=True, null=True)
    
    def __str__(self):
        return f"{self.customer.name} - {self.start_datetime} to {self.end_datetime}"