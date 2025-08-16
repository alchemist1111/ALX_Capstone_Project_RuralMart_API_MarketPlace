from .models import CartItem

def calculate_cart_total(cart):
    """
       Calculate the total price of all items in the given cart.
    """
    cart_items = CartItem.objects.filter(cart=cart)
    total = sum(item.total_price() for item in cart_items)
    return total


def calculate_cart_item_total(cart_item):
    """
      Calculate the total price for a specific cart item (product * quantity).
    """
    return cart_item.total_price()