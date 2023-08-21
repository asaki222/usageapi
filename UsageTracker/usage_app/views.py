from rest_framework import generics, status, serializers
from rest_framework.response import Response
from .serializers import AccumulatedUsageSerializer
from rest_framework.response import Response
import re
from django.core.exceptions import ObjectDoesNotExist

class AccumalatedUsageCreateView(generics.CreateAPIView):
    serializer_class = AccumulatedUsageSerializer
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            response = self.perform_create(serializer)
            if "No accumulated usage record or usage records found" in response:
                return Response(
                    {'message': 'Usage entry created successfully', 'accumulated_data': response},
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    {'message': response},
                     status=status.HTTP_404_NOT_FOUND
                )
        except serializers.ValidationError as e:
            if "Entry has already been processed" in str(e):
                error_detail = str(e.detail.get('error', ''))
                data_detail = str(e.detail.get('data', {}))
                data_string =  data_detail[1:-1].replace("\\'", "'")
                pattern = r"'(\w+)': ErrorDetail\(string='([^']+)'[^)]+\)"
                data_dict = dict(re.findall(pattern, data_string))
                return Response(
                    {'error': error_detail, 'data': data_dict},
                    status=status.HTTP_409_CONFLICT 
                )
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



    def perform_create(self, serializer):
        return serializer.save()