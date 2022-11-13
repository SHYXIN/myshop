"""myshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns

# urlpatterns = i18n_patterns(
#     path('admin/', admin.site.urls),
#     path('cart/', include('cart.urls', namespace='cart')),  # 购物车
#     path('orders/', include('orders.urls',namespace='orders')), # 订单
#     path('payment/', include('payment.urls', namespace='payment')), # 支付
#     path('coupon/', include('coupons.urls', namespace='coupons')), # 优惠券
#     path('rosetta/', include('rosetta.urls')),  # 翻译用
#     path('', include('shop.urls', namespace='shop')),  # 商店
# )


from django.utils.translation import gettext_lazy as _

urlpatterns = i18n_patterns(
    path(_('admin/'), admin.site.urls),
    path(_('cart/'), include('cart.urls', namespace='cart')),  # 购物车
    path(_('orders/'), include('orders.urls',namespace='orders')), # 订单
    path(_('payment/'), include('payment.urls', namespace='payment')), # 支付
    path(_('coupon/'), include('coupons.urls', namespace='coupons')), # 优惠券
    path('rosetta/', include('rosetta.urls')),  # 翻译用
    path('', include('shop.urls', namespace='shop')),  # 商店
)
