from django.urls import path
from .views import AccumalatedUsageCreateView

urlpatterns = [
    path('usage/create/', AccumalatedUsageCreateView.as_view(), name='usage-create'),
]
