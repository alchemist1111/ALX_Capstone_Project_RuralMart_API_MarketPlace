from django.contrib import admin
from .models import Category, Product

# Custom admin class for the Category model
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent_category', 'created_at', 'updated_at')  # Display relevant fields
    search_fields = ('name',)  # Allow searching by category name
    list_filter = ('parent_category',)  # Filter categories by parent category
    
    fieldsets = (
        (None, {
            'fields': ('name', 'parent_category')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',) 
        }),
    )

admin.site.register(Category, CategoryAdmin) 
admin.site.register(Product)   
