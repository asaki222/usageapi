from django.contrib import admin

from django.contrib import admin
from .models import Customer, Usage, AccumulatedUsage

admin.site.register(Customer)
admin.site.register(Usage)
admin.site.register(AccumulatedUsage)
