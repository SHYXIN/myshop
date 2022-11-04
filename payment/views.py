from django.shortcuts import render, redirect, get_object_or_404
import braintree
from django.conf import settings
from orders.models import Order
from .tasks import payment_completed

# Create your views here.
# 


# 实例化支付网关
gateway = braintree.BraintreeGateway(settings.BRAINTREE_CONF)

def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    total_cost = order.get_total_cost()
    # https://sandbox.braintreegateway.com/merchants/2bm456f7xp76j258/transactions/advanced_search
    # 信用卡设置
    # 4111 1111 1111 1111
    # 123
    # 12/28
    if request.method == 'POST':
        # 检索即时消息
        nonce = request.POST.get('payment_method_nonce', None)
        # create and submit transaction
        # print(gateway)
        result = gateway.transaction.sale({'amount': f'{total_cost:.2f}',
                                           'payment_method_nonce': nonce,
                                           'options':{
                                               'submit_for_settlement': True
                                           }
                                           })
        if result.is_success:
            # 支付成功
            order.paid = True
            # 保存唯一值
            order.braintree_id = result.transaction.id
            order.save()
            # 给客户发送发票
            payment_completed.delay(order.id)
            
            
            return redirect('payment:done')
        else:
            return redirect('payment:canceled')

    else:
        # 产生token
        client_token = gateway.client_token.generate()
        return render(request, 'payment/process.html', {'order': order,
                                                        'client_token':client_token,
                                                        })

def payment_done(request):
    return render(request,'payment/done.html')

def payment_canceled(request):
    return render(request, 'payment/canceled.html')