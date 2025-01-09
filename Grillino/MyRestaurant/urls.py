from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('register',views.register,name='register'),
    path('loginpw',views.loginPW,name='loginpw'),
    path('loginwithotp',views.loginwithotp,name='loginwithotp'),
    path('logout',views.logout_page,name='logout'),
    path('categories',views.category,name='categories'),
    path("products/<str:name>",views.products,name='products'),
    path('verifyotp/<int:user_id>',views.verify_otp,name='verifyotp'),
    path("update_item/",views.updateItem,name='update_item'),
    path('cart',views.cartpage,name='cart'),
    path("checkout",views.checkout,name='checkout'),
    path('save_shipping_address/',views.save_shipping_address,name='save_shipping_address'),
    path('orders',views.myorders,name='orders'),
    path('apply_coupon/', views.apply_coupon, name='apply_coupon'),
    path('booktable',views.bookatable,name='booktable'),
    path('profile',views.profile,name='profile'),
    path('profile_page/<str:id>',views.updateprofile,name='profile_page'),
    path('reviews',views.reviews,name='reviews'),
    path('search',views.Search,name='search')
]
