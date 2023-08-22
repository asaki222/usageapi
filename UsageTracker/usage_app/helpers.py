from decimal import Decimal
from .models import Usage, AccumulatedUsage
from datetime import datetime, time
from usage_app.utils import decimal_to_price


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

def calculate_total_price(usage_records):
        total_price = 0
        for usage in usage_records:
            price = Decimal(usage.price_per_unit) * usage.units_consumed
            total_price += price
            usage.processed = True
            usage.save()
        return total_price

def create_success_payload(acc, updated=False):
      message = 'Usage entry successful'
      return { 'message': message,
                'total_price': acc.price_in_dollars
             }

def update_or_create_accumulated_usage(customer, total_price):
        today = datetime.now().date()
        accumulated_usage = AccumulatedUsage.objects.filter(
                customer=customer,
                month=today.month,
                year=today.year
            )
    
        if len(accumulated_usage) != 0:
            accumulated_usage = accumulated_usage.first()
            accumulated_usage.accumulated_price += total_price
            accumulated_usage.price_in_dollars = decimal_to_price(total_price)
            accumulated_usage.save()
            return create_success_payload(accumulated_usage, updated=True)
        else:
            accumulated_usage = AccumulatedUsage.objects.create(
                customer=customer,
                month=today.month,
                year=today.year,
                accumulated_price=total_price,
                price_in_dollars=decimal_to_price(total_price)
    
            )
            return create_success_payload(accumulated_usage)