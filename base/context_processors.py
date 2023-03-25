from .models import Category, Order

def categories_processor(request):
    customer = request.user
    order_f = Order.objects.get(customer=customer, complete=False)
    categories = Category.objects.filter(parent=None)
    return {
            'categories': categories,
            'order_f':order_f
            }
