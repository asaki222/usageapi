from rest_framework import serializers
from .models import AccumulatedUsage, Usage
from usage_app.utils import decimal_to_price
from decimal import Decimal
from datetime import datetime

class AccumulatedUsageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccumulatedUsage
        fields = '__all__'
   
   
    def create(self, validated_data):
        try:
            customer = validated_data['customer']

            today = datetime.today()
            start_date = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            end_date = today.replace(day=31, month=today.month, hour=23, minute=59, second=59, microsecond=999999)
            usage_records = Usage.objects.filter(
                customer=customer,
                usage_date__range=(start_date, end_date),
                processed=False
            )
            
            if len(usage_records) == 0:
                try:
                    accumulated_usage = AccumulatedUsage.objects.get(
                        customer=customer,
                        start_datetime__month=today.month,
                        start_datetime__year=today.year
                    )
                    payload = AccumulatedUsageSerializer(accumulated_usage).data
                    raise serializers.ValidationError({
                        "error": f"Entry has already been processed for customer {customer.name}.",
                        "data": payload
                        }
                    )
                except AccumulatedUsage.DoesNotExist:
                    raise serializers.ValidationError({
                    "message": f"No accumulated usage record found for customer {customer.name}."
                })
            else:
                count_usage = 0
                count_price = 0
                starting_date_of_records = usage_records.first().usage_date
                ending_date_of_records = usage_records.last().usage_date
                for usage in usage_records:
                    price = Decimal(usage.price_per_unit) * usage.units_consumed
                    count_usage += usage.units_consumed
                    count_price += price
                    usage.processed = True
                    usage.save()

                try:
                    accumulated_usage = AccumulatedUsage.objects.get(
                    customer=customer,
                    start_datetime__month=today.month,
                    start_datetime__year=today.year
                        )
                except AccumulatedUsage.DoesNotExist:
                        accumulated_usage = None

                if accumulated_usage:
                    accumulated_usage.accumulated_units += count_usage
                    accumulated_usage.accumulated_price += count_price
                    accumulated_usage.save()
                else:
                    accumulated_usage = AccumulatedUsage.objects.create(
                            customer=customer,
                            start_datetime=starting_date_of_records,
                            end_datetime=ending_date_of_records,
                            accumulated_units=count_usage,
                            accumulated_price=count_price
                        )
                    accumulated_usage.save()
                
                
                accumulated_usage.price_in_dollars  = decimal_to_price(accumulated_usage.accumulated_price)
                accumulated_usage.save()
                return AccumulatedUsageSerializer(accumulated_usage).data
        except serializers.ValidationError as ve:
            raise ve 
        except Exception as e:
            error_message = str(e)
            raise serializers.ValidationError(error_message)

