from rest_framework import serializers
from .models import AccumulatedUsage
from usage_app.utils import decimal_to_price
from .helpers import calculate_total_usage_and_price, update_or_create_accumulated_usage, get_unprocessed_usage_records, get_month_start_end_dates
from datetime import datetime

class AccumulatedUsageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccumulatedUsage
        fields = '__all__'
   
   
    def create(self, validated_data):
        try:
            customer = validated_data['customer']

            start_date, end_date = get_month_start_end_dates()
            usage_records = get_unprocessed_usage_records(customer, start_date, end_date)
            
            if len(usage_records) == 0:
                raise self.handle_processed_entry_error(customer)
            else:
                total_usage, total_price = calculate_total_usage_and_price(usage_records)
                accumulated_usage = update_or_create_accumulated_usage(customer, total_usage, total_price)
                accumulated_usage.price_in_dollars = decimal_to_price(accumulated_usage.accumulated_price)
                accumulated_usage.save()
                return AccumulatedUsageSerializer(accumulated_usage).data
        except serializers.ValidationError as ve:
            raise ve 
        except Exception as e:
            error_message = str(e)
            raise serializers.ValidationError(error_message)
        

    #didnt move this method to the helpers file due to circular input
    def handle_processed_entry_error(self, customer):
        try:
            today = datetime.today()
            accumulated_usage = AccumulatedUsage.objects.get(
                customer=customer,
                start_datetime__month=today.month,
                start_datetime__year=today.year
            )
            payload = AccumulatedUsageSerializer(accumulated_usage).data
            raise serializers.ValidationError({
                "error": f"Entry has already been processed for customer {customer.name}.",
                "data": payload
            })
        except AccumulatedUsage.DoesNotExist:
            raise serializers.ValidationError({
                "message": f"No accumulated usage record found for customer {customer.name}."
            })