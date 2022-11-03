from io import BytesIO
from celery import task
import weasyprint
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from orders.models import Order

@task
def payment_completed(order_id):
    """
    Task to send an e-mail notification when an order is
    successfully created.
    """
    order = Order.objects.get(id=order_id)
    # 创建发票邮件

    subject = f'My shop - EE Invoice no. {order_id}'
    message =  'Please, find attached the invoice for your recent purchase.'
    email = EmailMessage(subject, 
                         message,
                         'admin@myshop.com',
                         [order.email],
                         )
    # 生成pdf
    html = render_to_string('orders/order/pdf.html', {'order': order})
    out = BytesIO()
    stylesheets = [weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css')]
    weasyprint.HTML(string=html).write_pdf(out, stylesheets=stylesheets)

    # 附上附件pdf
    email.attach(f'order_{order_id}.pdf',out.getvalue(), 'application/pdf')
    
    # 发送邮件
    email.send()
    