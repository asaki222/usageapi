from rest_framework import generics, status, serializers
from rest_framework.response import Response
from .serializers import AccumulatedUsageSerializer
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
import re

class AccumalatedUsageCreateView(generics.CreateAPIView):
    serializer_class = AccumulatedUsageSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        accumulated_data = None 
        try:
            accumulated_data = self.perform_create(serializer)
        except serializers.ValidationError as e:
            if "Entry has already been processed" in str(e):
                error_detail = str(e.detail.get('error', ''))
                data_detail = str(e.detail.get('data', {}))
                data_string =  data_detail[1:-1].replace("\\'", "'")
                pattern = r"'(\w+)': ErrorDetail\(string='([^']+)'[^)]+\)"
                data_dict = dict(re.findall(pattern, data_string))
                return Response(
                    {'error': error_detail,
                     'data': data_dict},
                    status=status.HTTP_409_CONFLICT 
                )
            else:
                return Response(
                    {'error': str(e)},
                    status=status.HTTP_400_BAD_REQUEST
            )
        
        return Response(
            {'message': 'Usage entry created successfully', 'accumulated_data': accumulated_data},
            status=HTTP_201_CREATED
        )


    def perform_create(self, serializer):
        return serializer.save()