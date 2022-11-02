from django.shortcuts import render
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created
# Create your views here.


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'],
                                         )
                # 清空购物车
                cart.clear()
                # 启动异步任务
                # pip install eventlet
                # celery -A myshop  worker -l info  --pool=solo
                order_created.delay(order.id)
                
                # 监控celcery
                # pip install flower==0.9.3
                # celery -A myshop flower
                # https://stackoverflow.com/questions/62975722/error-executing-flower-with-celery-in-windows-10
                # import sys
                # if sys.platform == 'win32':
                #     asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())                #
                
                return render(request, 'orders/order/created.html', {'order': order})
    else:
        form = OrderCreateForm()
    return render(request, 'orders/order/create.html', {'cart': cart,
                                                        'form': form,
                                                        })