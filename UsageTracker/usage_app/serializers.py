from rest_framework import serializers
from .models import AccumulatedUsage
from .helpers import calculate_total_price, update_or_create_accumulated_usage, get_unprocessed_usage_records, get_month_start_end_dates
from datetime import datetime
from usage_app.exceptions import NetworkError, ValidationError

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
                error_message, total_price = self.handle_processed_empty_records(customer)
                return {
                    "message": error_message,
                    "total_price": total_price
                }
            else:
                total_price = calculate_total_price(usage_records)
                accumulated_usage = update_or_create_accumulated_usage(customer, total_price)                
                return accumulated_usage
        except ValidationError as ve:
            raise ve 
        except NetworkError as e:
            error_message = str(e)
            raise serializers.ValidationError(error_message)


    #didnt move this method to the helpers file due to circular input
    def handle_processed_empty_records(self, customer):
        today = datetime.now().date()
        accumulated_usage = AccumulatedUsage.objects.filter(
                customer=customer,
                month=today.month,
                year=today.year
        )
        if len(accumulated_usage) == 0:
            error_message = f"No accumulated usage record or usage records found for customer."
            payload = {}
            return error_message, payload
        else:
            accumulated_usage = accumulated_usage.first()
            error_message = f"Entry has already been processed for customer {customer.name}."
            return error_message, accumulated_usage.price_in_dollars