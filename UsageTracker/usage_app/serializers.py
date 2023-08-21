from rest_framework import serializers
from .models import AccumulatedUsage
from usage_app.utils import decimal_to_price
from .helpers import calculate_total_usage_and_price, update_or_create_accumulated_usage, get_unprocessed_usage_records, get_month_start_end_dates
from datetime import datetime
from usage_app.exceptions import NetworkError, ValidationError

class AccumulatedUsageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccumulatedUsage
        fields = '__all__'
   
   
    def create(self, validated_data):
        try:
            customer = validated_data['customer']
            print(customer)

            start_date, end_date = get_month_start_end_dates()
            print('we got the dates')
            usage_records = get_unprocessed_usage_records(customer, start_date, end_date)
            print('we got the records')
            print(len(usage_records))
            if len(usage_records) == 0:
                print('no records')
                error_message = self.handle_processed_entry_error(customer)
                raise serializers.ValidationError({
                    "error": error_message,
                })
            else:
                print('saving records dd')
                total_usage, total_price = calculate_total_usage_and_price(usage_records)
                print('we finished calcu', total_price, total_price)
                accumulated_usage = update_or_create_accumulated_usage(customer, total_usage, total_price)
                print('we have the usage now', accumulated_usage)
                accumulated_usage.price_in_dollars = decimal_to_price(accumulated_usage.accumulated_price)
                print('we made it here to after calculating the price in dollars')
                accumulated_usage.save()
                print('usage', accumulated_usage)
                return AccumulatedUsageSerializer(accumulated_usage).data
        except ValidationError as ve:
            raise ve 
        except NetworkError as e:
            error_message = str(e)
            raise serializers.ValidationError(error_message)


    #didnt move this method to the helpers file due to circular input
    def handle_processed_entry_error(self, customer):
        try:
            today = datetime.now().date()
            accumulated_usage = AccumulatedUsage.objects.get(
                customer=customer,
                month=today.month,
                year=today.year
            )
            payload = AccumulatedUsageSerializer(accumulated_usage).data
            error_message = f"Entry has already been processed for customer {customer.name}."
            return error_message, payload
        except AccumulatedUsage.DoesNotExist:
            error_message = f"No accumulated usage record or usage records found for customer {customer.name}."
            return error_message, None