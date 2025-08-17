import django_filters
from .models import Product, Category

class ProductFilter(django_filters.FilterSet):
    # Filter by price range
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte', label='Minimum price')
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr='lte', label='Maximum price')
    
    # Filter by category
    category = django_filters.ModelChoiceFilter(queryset=Category.objects.all(), label='Category')
    
    # Searching in name or description
    search = django_filters.CharFilter(field_name='name', lookup_expr='icontains', label='Search')
    
    # Ordering by multiple fields
    ordering = django_filters.OrderingFilter(
        fields = (
            ('price', 'price'),
            ('created_at', 'created_at'),
            ('name', 'name'),
        ),
        label='Ordering'
    )
    
    class Meta:
        model = Product
        fields = ['category', 'min_price', 'max_price', 'search']