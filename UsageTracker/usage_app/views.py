from rest_framework import generics, status, serializers
from rest_framework.response import Response
from .serializers import AccumulatedUsageSerializer
from .serializers import AccumulatedUsageSerializer

class AccumalatedUsageCreateView(generics.CreateAPIView):
    serializer_class = AccumulatedUsageSerializer
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            response = self.perform_create(serializer)
            return self.handle_response(response)
        except Exception as e:
            return Response({"error": "An unexpected error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def handle_response(self, response):
        message = response['message']
        if "Usage entry successful" in message:
            return Response(
                {'message': message, 'total_price': response['total_price']},
                status=status.HTTP_201_CREATED
            )
        elif "Entry has already been processed" in message:
            return Response(
                {'message': message, 'total_price': response['total_price']},
                status=status.HTTP_409_CONFLICT
            )
        elif "No accumulated usage record or usage records found" in message:
            return Response(
                {'message': message},
                status=status.HTTP_404_NOT_FOUND
            )

    def perform_create(self, serializer):
        return serializer.save()