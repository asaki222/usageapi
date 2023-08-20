from decimal import Decimal
from datetime import datetime
from .models import Usage, AccumulatedUsage


def get_month_start_end_dates():
        today = datetime.today()
        start_date = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        end_date = today.replace(day=31, month=today.month, hour=23, minute=59, second=59, microsecond=999999)
        return start_date, end_date
    
def get_unprocessed_usage_records(customer, start_date, end_date):
        return Usage.objects.filter(
            customer=customer,
            usage_date__range=(start_date, end_date),
            processed=False
        )
        

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
    
def update_or_create_accumulated_usage(customer, total_usage, total_price, usage_records):
        today = datetime.today()
        try:
            accumulated_usage = AccumulatedUsage.objects.get(
                customer=customer,
                start_datetime__month=today.month,
                start_datetime__year=today.year
            )
            accumulated_usage.accumulated_units += total_usage
            accumulated_usage.accumulated_price += total_price
            accumulated_usage.save()
        except AccumulatedUsage.DoesNotExist:
            starting_date_of_records = usage_records.first().usage_date
            ending_date_of_records = usage_records.last().usage_date
            accumulated_usage = AccumulatedUsage.objects.create(
                customer=customer,
                start_datetime=starting_date_of_records,
                end_datetime=ending_date_of_records,
                accumulated_units=total_usage,
                accumulated_price=total_price
            )
            accumulated_usage.save()
        return accumulated_usage