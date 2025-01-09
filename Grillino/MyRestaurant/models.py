from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
import datetime
import os

#Compress Image
from PIL import Image
from django.core.files.base import ContentFile
from io import BytesIO

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self,email,password,**extra_fields):
        if not email:
            raise ValueError('Email is not given')
        email = self.normalize_email(email)
        user = self.model(email = email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self,email,password,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active',True)

        if not extra_fields.get('is_staff'):
            raise ValueError('Superuser must have is_staff = True')
        
        if not extra_fields.get('is_superuser'):
            raise ValueError('Superuser must have is_superuser = True')
        
        return self.create_user(email,password,**extra_fields)
        

class CustomUser(AbstractBaseUser):
    email = models.EmailField(max_length=254,unique=True)
    password = models.CharField(max_length=254,null=False)
    first_name = models.CharField(max_length=255,null=False,blank=False)
    last_name = models.CharField(max_length=255,null=False,blank=False)
    mobile = models.CharField(max_length=15,null=True,blank=False,unique=True)
    is_email_verified = models.BooleanField(default=False)
    otp = models.IntegerField(null=True,blank=True)
    address = models.CharField(max_length=200,null=True,blank=True)
    city = models.CharField(max_length=100,null=True,blank=True)
    state = models.CharField(max_length=100,null=True,blank=True)
    pincode = models.IntegerField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_short_name(self):
        return self.first_name
    
    def has_module_perms(self,app_label):
        return True
    
    def has_perm(self,perm,obj=None):
        return True
    
    def get_all_permissions(self, obj=None):
        # Implement logic to get all permissions for this user
        return []
    

def getFilename(request, filename):
    now_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")  # Fix the time formatting (remove colon)
    new_file = '%s%s' % (now_time, filename)
    return os.path.join('Media/', new_file)

class Category(models.Model):
    name = models.CharField(max_length=150, null=False, blank=False)
    image = models.ImageField(upload_to=getFilename, null=True, blank=True)
    description = models.TextField(max_length=500, null=False, blank=False)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    @property
    def Imageurl(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    
    def compress_image(self):
        """Compress the image to reduce file size."""
        img = Image.open(self.image)

        # Resize image (optional, to a maximum size, e.g., 1024x1024)
        img.thumbnail((1024, 1024))

        # Create a BytesIO object to save the compressed image
        temp_image = BytesIO()
        img.save(temp_image, format='JPEG', quality=75, optimize=True)
        temp_image.seek(0)

        # Save the compressed image to the file storage
        self.image.save(self.image.name, ContentFile(temp_image.read()), save=False)
    
    def save(self, *args, **kwargs):
        """Override the save method to compress image before saving."""
        if self.image:
            self.compress_image()
        super().save(*args, **kwargs)

    
class Product(models.Model):
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    name=models.CharField(max_length=150,null=False,blank=False)
    vendor=models.CharField(max_length=150,null=False,blank=False,default="Grillino")
    product_image=models.ImageField(upload_to=getFilename,null=True,blank=True)
    selling_price=models.FloatField(null=False,blank=False)
    description=models.TextField(max_length=750,null=False,blank=False,default="Tasty and Yummy")
    trending=models.BooleanField(default=False,help_text="0-default,1-trending")
    created_at=models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    @property
    def Imageurl(self):
        try:
            url=self.product_image.url
        except:
            url=''
        return url
    
    def compress_image(self):
        """Compress the image to reduce file size."""
        img = Image.open(self.product_image)

        # Resize image (optional, to a maximum size, e.g., 1024x1024)
        img.thumbnail((1024, 1024))

        # Create a BytesIO object to save the compressed image
        temp_image = BytesIO()
        img.save(temp_image, format='JPEG', quality=75, optimize=True)
        temp_image.seek(0)

        # Save the compressed image to the file storage
        self.product_image.save(self.product_image.name, ContentFile(temp_image.read()), save=False)
    
    def save(self, *args, **kwargs):
        """Override the save method to compress image before saving."""
        if self.product_image:
            self.compress_image()
        super().save(*args, **kwargs)


class Order(models.Model):
    customer=models.ForeignKey(CustomUser,on_delete=models.SET_NULL, null=True,blank=True)
    date_ordered=models.DateTimeField(auto_now_add=True)
    complete=models.BooleanField(null=True,blank=False,default=False)
    transaction_id=models.CharField(max_length=50,null=True)

    def __str__(self):
        return str(self.id)
    
    @property
    def get_cart_total(self):
        orderitems=self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    
    @property
    def get_cart_items(self):
        orderitems=self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
    
    @property
    def get_cart(self):
        total = self.orderitem_set.count()
        return total
    
class OrderItem(models.Model):
    product=models.ForeignKey(Product,on_delete=models.SET_NULL,null=True,blank=True)
    order=models.ForeignKey(Order,on_delete=models.SET_NULL,null=True,blank=True)
    quantity=models.IntegerField(default=0,null=True,blank=True)
    date_added=models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        if self.product:
            total = self.product.selling_price * self.quantity
            return total
        return 0
    
class ShippingAddress(models.Model):
    customer=models.ForeignKey(CustomUser,on_delete=models.SET_NULL,null=True,blank=True)
    order=models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
    address=models.CharField(max_length=300,null=True)
    city=models.CharField(max_length=100,null=True)
    state=models.CharField(max_length=100,null=True)
    zipcode=models.CharField(max_length=50,null=True)
    date_added=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
    
class Coupon(models.Model):
    code = models.CharField(max_length=20, unique=True)  # Coupon code
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)  # Discount percentage
    max_usage = models.PositiveIntegerField()  # Max number of uses
    used_count = models.PositiveIntegerField(default=0)  # How many times the coupon has been used
    expiration_date = models.DateTimeField(null=True, blank=True)  # Optional expiration date
    
    def __str__(self):
        return self.code
    
class BookaTable(models.Model):
    first_name = models.CharField(max_length=50,null=False,blank=False)
    last_name = models.CharField(max_length=50,null=True,blank=True)
    email = models.EmailField(max_length=100,null=False,blank=False)
    phone_number = models.IntegerField(null=False,blank=False)
    date = models.DateTimeField(null=False,blank=False)
    count = models.IntegerField(null=True,blank=True)

    def __str__(self):
        return self.first_name
    
class Reviews(models.Model):
    customer = models.CharField(max_length=100,null=False,blank=False)
    about = models.CharField(max_length=100,null=False,blank=False)
    rating = models.IntegerField(null=False,blank=False)
    comment = models.CharField(max_length=500,null=True,blank=True)

    def __str__(self):
        return self.customer
