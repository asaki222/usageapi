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
        print('beginning of calcualating')
        total_usage = 0
        total_price = 0
        for usage in usage_records:
            price = Decimal(usage.price_per_unit) * usage.units_consumed
            total_usage += usage.units_consumed
            total_price += price
            usage.processed = True
            usage.save()
        print('finished calculating')
        return total_usage, total_price
    
def update_or_create_accumulated_usage(customer, total_usage, total_price):
        print('we are getting into creating a new record')
        today = datetime.now().date()
        try:
            print('we trying it')
            accumulated_usage = AccumulatedUsage.objects.get(
                customer=customer,
                month=today.month,
                year=today.year
            )
            accumulated_usage.accumulated_units += total_usage
            accumulated_usage.accumulated_price += total_price
            print('we aabout to save the record')
            accumulated_usage.save()
            print('we saved it')
        except AccumulatedUsage.DoesNotExist:
            print('we never found usage or a record')
            accumulated_usage = AccumulatedUsage.objects.create(
                customer=customer,
                month=today.month,
                year=today.year,
                accumulated_units=total_usage,
                accumulated_price=total_price
            )
            print('after record was created')
            print('we saved a record', accumulated_usage)
            return accumulated_usage