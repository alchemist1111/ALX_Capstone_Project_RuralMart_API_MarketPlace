from django.contrib import admin
from .models import Payment, PaymentMethod, Transaction

admin.site.register(Payment)
admin.site.register(PaymentMethod)
admin.site.register(Transaction)
