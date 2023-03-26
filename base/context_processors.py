from .models import Category, Order

def categories_processor(request):
    order_f = None
    if request.user.is_authenticated:
        customer = request.user
        try:
            order_f = Order.objects.get(customer=customer, complete=False)
        except Order.DoesNotExist:
            pass
    categories = Category.objects.filter(parent=None)
    return {
            'categories': categories,
            'order_f':order_f
            }
