import pyotp
from datetime import datetime, timedelta
from .models import *

def generate_otp():
    totp = pyotp.TOTP(pyotp.random_base32(), interval=300)  # 5 minutes validity
    return totp.now()

def cartData(request):
     if request.user.is_authenticated:
          customer = request.user
          order,created = Order.objects.get_or_create(customer=customer,complete=False)
          items = order.orderitem_set.all()
          cartitems = order.get_cart
     else:
          items = 0
          cartitems = 0
          order = 0
        #   cookieData = cookieCart(request)
        #   cartitems = cookieData['cartitems']
        #   order = cookieData['order']
        #   items = cookieData['items']
     return{'items':items,'order':order,'cartitems':cartitems}


