from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created
from django.contrib.admin.views.decorators import staff_member_required
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.conf import settings
import weasyprint

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
                
                request.session['order_id'] = order.id
                
                # return render(request, 'orders/order/created.html', {'order': order})
                return redirect(reverse('payment:process'))
    else:
        form = OrderCreateForm()
    return render(request, 'orders/order/create.html', {'cart': cart,
                                                        'form': form,
                                                        })
    

@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'admin/orders/order/detail.html',{'order': order})


@staff_member_required
def admin_order_pdf(request, order_id):
    # pip install WeasyPrint==51
    # gtk下载https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases
    # python manage.py collectstatic
        
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('orders/order/pdf.html', {'order': order})

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{order_id}.pdf'

    weasyprint.HTML(string=html).write_pdf(response, 
                                           stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css')])

    return response