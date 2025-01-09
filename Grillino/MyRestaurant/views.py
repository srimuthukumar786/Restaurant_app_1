from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.contrib import messages
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.hashers import make_password  # Import make_password function
from django.core.mail import send_mail
from django.conf import settings
from .utils import *
import json
from django.http import JsonResponse
from decimal import Decimal

# Create your views here.
def index(request):
    data = Product.objects.filter(trending = 1)
    cartdata = cartData(request)
    cartitems = cartdata['cartitems']
    reviews = Reviews.objects.all()
    return render(request,'index.html',{'data':data,'cartitems':cartitems,'reviews':reviews})

def register(request):
    cartdata = cartData(request)
    cartitems = cartdata['cartitems']
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('pass')
        if CustomUser.objects.filter(email = email):
            messages.warning(request,'User Already Exist!')
         # Hash the password before saving
        hashed_password = make_password(password)  # Hash the password using Django's built-in function

        user = CustomUser(email = email,password = hashed_password, first_name = fname, last_name = lname, mobile = phone)
        user.save()
        messages.warning(request,'User Registered Successfully!')
        return redirect('loginpw')

    return render(request, 'register.html',{'cartitems':cartitems})

def loginPW(request):
    cartdata = cartData(request)
    cartitems = cartdata['cartitems']
    if request.user.is_authenticated:
         return redirect('/')
    else:
         if request.method == 'POST':
          email=request.POST.get('email')
          password=request.POST.get('password')
          user=authenticate(request,email=email,password=password)
          if user is not None:
               login(request,user)
               messages.success(request,'Login Successfully!')
               return redirect('/')
          else:
            messages.warning(request,'Invalid Username and Password!')
            return redirect('loginpw')
    return render(request,'login.html',{'cartitems':cartitems})

def logout_page(request):
   if request.user.is_authenticated:
      logout(request)
      messages.success(request,'Logout Successfully!')
   return redirect('/')

def category(request):
    data = Category.objects.all()
    cartdata = cartData(request)
    cartitems = cartdata['cartitems']
    return render(request,'categories.html',{'data':data,'cartitems':cartitems})

def products(request,name):
    cartdata = cartData(request)
    cartitems = cartdata['cartitems']
    sort_option = request.POST.get('sort', '')
    if Category.objects.filter(name = name):
        data = Product.objects.filter(category__name=name)
         # Apply sorting based on the sort option
        if sort_option == 'low_to_high':
            data = data.order_by('selling_price')  # Sort low to high
        elif sort_option == 'high_to_low':
            data = data.order_by('-selling_price')  # Sort high to low
        return render(request,'products.html',{'data':data,'cname':name,'cartitems':cartitems})
    else:
        return redirect('categories')


def loginwithotp(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            # Try to fetch the user by email
            user = CustomUser.objects.get(email=email)
            if not user:
                messages.error(request, 'User Not Found!')
                return redirect('register')
            
            # Generate and save OTP
            email_otp = generate_otp()
            print(email_otp)
            user.otp = email_otp
            user.save()  # Ensure the OTP is saved to the database
            
            # Send email OTP
            send_mail(
                'Email Verification OTP',
                f'Your OTP for email verification is: {email_otp}',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            # Optionally redirect to verify OTP page
            return redirect('verifyotp', user_id=user.id)

        except CustomUser.DoesNotExist:
            messages.error(request, 'User Not Found!')
            return redirect('register')

    return render(request, 'loginwithotp.html')

def verify_otp(request, user_id):
    user = CustomUser.objects.get(id=user_id)

    if request.method == 'POST':
        email_otp = request.POST.get('otp')
        print(type(email_otp))
        print(type(user.otp))

        if email_otp == str(user.otp):
            user.is_email_verified = True
            user.otp = None  # Clear OTP after successful verification
            user.save()

            # Log the user in and redirect to the homepage
            login(request, user)
            return redirect('/')

        else:
            # If OTP is invalid, show an error
            return render(request, 'verifyotp.html', {'error': 'Invalid OTP'})

    return render(request, 'verifyotp.html')

def updateItem(request):
     data =  json.loads(request.body)
     productId = data['productId']
     action = data['action']
     
     print('Action:',action)
     print('productId:',productId)

     customer=request.user
     product = Product.objects.get(id = productId)
     order,created = Order.objects.get_or_create(customer=customer,complete=False)

     orderItem,created = OrderItem.objects.get_or_create(order = order, product = product)
     

     if action == 'add':
          orderItem.quantity = (orderItem.quantity + 1)
     if action == 'remove':
          orderItem.quantity = (orderItem.quantity - 1)
     orderItem.save()
     if action == 'delete':
         orderItem.delete()
     
     if orderItem.quantity <=0:
          orderItem.delete()

     return JsonResponse('Item was added',safe=False)

def cartpage(request):
     if request.user.is_authenticated:
        customer = request.user
        order,created = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
        cartitems = order.get_cart
        return render(request,'cartpage.html',{'items':items,'order':order,'cartitems':cartitems})
     else:
         return JsonResponse('Login to check cart!',safe=False)

def checkout(request):
     coupon_code = Coupon.objects.all().first()
     try:
        coupon = Coupon.objects.get(code=coupon_code)
        discount = coupon.discount_percentage
        coupon_used_count = coupon.used_count
        coupon_max_usage = coupon.max_usage
     except Coupon.DoesNotExist:
        coupon_used_count = 0
        coupon_max_usage = 0
     data = cartData(request)
     items = data['items']
     order = data['order']
     cartitems = data['cartitems']
     return render(request,'checkout.html',{'items':items,'order':order,'cartitems':cartitems,'coupon':coupon_code,'discount':discount,'coupon_used_count': coupon_used_count,'coupon_max_usage': coupon_max_usage})

def save_shipping_address(request): 
    if request.method == 'POST':
        # Get the data from the request body
        data = json.loads(request.body)
        razorpay_payment_id = data.get('razorpay_payment_id')
        print(data)
        
        # Check if the user is logged in
        if request.user.is_authenticated:
            # If logged in, associate the address with the current user
            user = request.user
            order, created = Order.objects.get_or_create(customer=user, complete=False)

        order.transaction_id = razorpay_payment_id
        order.complete = True
        order.save()
        
        # Save the shipping address details (assuming you have a ShippingAddress model)
        shipping_address = ShippingAddress(
            customer=user,
            order = order,
            address=data['address'],
            city=data['city'],
            state=data['state'],
            zipcode=data['zipcode']
        )
        shipping_address.save()

        # Assuming cart is stored in the user's session, clear it
        # request.session['cart'] = {}  # Clear the cart session variable

        return JsonResponse({"success": True})
    
    return JsonResponse({"error": "Invalid request"}, status=400)

def myorders(request):
    datas = cartData(request)
    cartitems = datas['cartitems']
    # Fetch all completed orders for the logged-in user
    orders = Order.objects.filter(customer=request.user, complete=True)

    # If orders exist, get all order items related to those orders
    if orders.exists():
        myorder = OrderItem.objects.filter(order__in=orders)  # Fetch all OrderItems related to the orders
    else:
        myorder = None  # or you can pass an empty list if you prefer

    return render(request, 'orders.html', {'items': myorder, 'cartitems': cartitems})

def apply_coupon(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        coupon_code = data.get('coupon_code')
        total = Decimal(data.get('total'))  # Ensure 'total' is a Decimal
        
        try:
            # Validate the coupon by checking max_usage and used_count
            coupon = Coupon.objects.get(code=coupon_code)
            
            # Check if the coupon has available usage left
            if coupon.used_count >= coupon.max_usage:
                return JsonResponse({
                    'success': False,
                    'message': 'Coupon usage limit reached.'
                })

            # Convert discount_percentage to Decimal (if it is a float, convert it)
            discount_percentage = Decimal(coupon.discount_percentage)

            # Calculate the discount amount (convert both to Decimal for precision)
            discount_amount = (discount_percentage / Decimal(100)) * total
            new_total = total - discount_amount

            # Update the used_count for the coupon
            coupon.used_count += 1
            coupon.save()
            
            return JsonResponse({
                'success': True,
                'new_total': new_total,
            })
        except Coupon.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Invalid coupon code.'
            })

    return JsonResponse({'success': False, 'message': 'Invalid request'})

def bookatable(request):
    datas = cartData(request)
    cartitems = datas['cartitems']
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        date = request.POST.get('date')
        count = request.POST.get('count')

        book = BookaTable(first_name=fname,last_name=lname,email=email,phone_number=phone,date=date,count=count)
        book.save()
        # Send email OTP
        send_mail(
            'Booking Status',
            f'Dear {fname},your table has been booked for {count} person successfully',
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
        # Optionally redirect to verify OTP page
        return redirect('/')
    return render(request,'booktable.html',{'cartitems': cartitems})

def profile(request):
    datas = cartData(request)
    cartitems = datas['cartitems']
    if request.user.is_authenticated:
        profile = CustomUser.objects.get(email = request.user)
        return render(request,'profile.html',{'profile':profile,'cartitems': cartitems})
    
def updateprofile(request, id):
    profile = get_object_or_404(CustomUser, id=id)  # Get the profile or return a 404 if not found
    if request.method == 'POST':
        if 'fname' in request.POST:
            profile.first_name = request.POST['fname']
        if 'lname' in request.POST:
            profile.last_name = request.POST['lname']
        if 'phone' in request.POST:
            profile.mobile = request.POST['phone']
        if 'address' in request.POST:
            profile.address = request.POST['address']
        if 'city' in request.POST:
            profile.city = request.POST['city']
        if 'state' in request.POST:
            profile.state = request.POST['state']
        if 'pincode' in request.POST:
            profile.pincode = request.POST['pincode']
        
        
        # Save the profile data after updates
        profile.save()
        
        # Add a success message
        messages.success(request, 'Profile updated successfully')

        # Return to the same page with the updated data
        return redirect('profile')

    # If GET request, render the page with current profile data
    return render(request, 'profile.html', {'profile':profile})

def reviews(request):
    datas = cartData(request)
    cartitems = datas['cartitems']
    products = Product.objects.all()
    if request.method == 'POST':
        customer = request.user.first_name
        about = request.POST.get('about')
        rating = request.POST.get('rating')
        review_text = request.POST.get('reviewText')
        feedback = Reviews(customer = customer,about = about, rating = rating, comment = review_text)
        feedback.save()
        messages.success(request, 'Feedback updated successfully')
        return redirect('orders')
    return render(request,'reviews.html',{'products': products,'cartitems': cartitems})

def Search(request):
    datas = cartData(request)
    cartitems = datas['cartitems']
    if request.method == 'POST':
        keyword = request.POST.get('keyword')
        sort_option = request.POST.get('sort', '')
        if keyword == 'veg':
            categories = Category.objects.filter(name__in=['Vegetarian', 'Veg Starters'])
        else:
            categories = Category.objects.filter(name__icontains=keyword)
        if categories.exists():
            products = Product.objects.filter(category__in=categories)
        else:
            products = Product.objects.filter(name__icontains=keyword)
        
         # Apply sorting based on the sort option
        if sort_option == 'low_to_high':
            products = products.order_by('selling_price')  # Sort low to high
        elif sort_option == 'high_to_low':
            products = products.order_by('-selling_price')  # Sort high to low
        return render(request,'search.html',{'keyword':keyword,'products':products,'cartitems': cartitems})