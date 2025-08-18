from django.contrib import admin
from .models import Order, OrderItem

# Order Admin
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'order_date', 'status', 'total_amount']
    list_filter = ['status', 'order_date']
    search_fields = ['user__first_name', 'user__last_name']
    
# OrderItem Admin    
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'quantity', 'unit_price')
    search_fields = ('order__id', 'product__name')
    list_filter = ('order__status', 'product')
    ordering = ('order__id',)  
    
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)      
    
