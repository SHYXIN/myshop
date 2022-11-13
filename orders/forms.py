from django import forms
from localflavor.us.forms import USZipCodeField  # 美国邮政编码 
from localflavor.cn.forms import CNPostCodeField # 中国邮政编码
from .models import Order

class OrderCreateForm(forms.ModelForm):
    postal_code = CNPostCodeField()  
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'postal_code', 'city']

    