from celery import task
from django.core.mail import send_mail
from .models import Order

@task
def order_created(order_id):
    """
    在成功创建订单时,发送电子邮件通知的任务。
    """
    order = Order.objects.get(id=order_id)
    subject = f'订单号：{order.id}'
    message = f'亲爱的{order.first_name},\n\n'\
        f'你成功下单了，订单号是{order.id}'
    mail_sent = send_mail(subject,
                          message,
                          'admin@myshop.com',
                          [order.email],
                          )
    return mail_sent
