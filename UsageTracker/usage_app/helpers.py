from decimal import Decimal
from .models import Usage, AccumulatedUsage
from datetime import datetime, time


def get_month_start_end_dates():
        today = datetime.now().date()
        start_date = datetime.combine(today.replace(day=1), time(0, 0))
        end_date = datetime.combine(today.replace(day=31), time(23, 59, 59, 999999))

        return start_date, end_date
    
def get_unprocessed_usage_records(customer, start_date, end_date):
        records = Usage.objects.filter(
            customer=customer,
            usage_date__range=(start_date, end_date),
            processed=False
        )
        return records
        

def calculate_total_usage_and_price(usage_records):
        total_usage = 0
        total_price = 0
        for usage in usage_records:
            price = Decimal(usage.price_per_unit) * usage.units_consumed
            total_usage += usage.units_consumed
            total_price += price
            usage.processed = True
            usage.save()
        return total_usage, total_price
    
def update_or_create_accumulated_usage(customer, total_usage, total_price):
        today = datetime.now().date()
        try:
            accumulated_usage = AccumulatedUsage.objects.get(
                customer=customer,
                month=today.month,
                year=today.year
            )
            accumulated_usage.accumulated_units += total_usage
            accumulated_usage.accumulated_price += total_price
            accumulated_usage.save()
        except AccumulatedUsage.DoesNotExist:
            accumulated_usage = AccumulatedUsage.objects.create(
                customer=customer,
                month=today.month,
                year=today.year,
                accumulated_units=total_usage,
                accumulated_price=total_price
            )
            return accumulated_usage