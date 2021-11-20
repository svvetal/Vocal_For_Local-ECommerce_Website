from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)
    address = models.CharField(max_length=200 , null=True , blank=True)
    joined_on = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.full_name

class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)
    address = models.CharField(max_length=200, null=True , blank=True)
    shop_name = models.CharField(max_length=200, null=True , blank=True)
    shop_id = models.PositiveIntegerField()
    joined_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name

class Category(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title

class Product(models.Model):
    title = models.CharField(max_length=200)
    slug = models.CharField(max_length=100 , unique=True)
    category = models.ForeignKey(Category , on_delete=models.CASCADE)
    image = models.ImageField(upload_to="products")
    marked_price = models.PositiveBigIntegerField()
    selling_price = models.PositiveIntegerField()
    stock = models.PositiveIntegerField(default = 1)
    description = models.TextField()
    warranty = models.CharField(max_length=300 , null=True, blank=True)
    view_count = models.PositiveIntegerField(default=0)
    id = models.PositiveBigIntegerField(primary_key=True)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE,default = 1)
    def __str__(self):
        return self.title

class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL , null=True , blank=True)
    total = models.PositiveBigIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Cart : " + str(self.id)

class CartProduct(models.Model):
    cart = models.ForeignKey(Cart , on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rate = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    subtotal = models.PositiveIntegerField()

    def __str__(self):
        return "Cart : " + str(self.cart.id) + "CartProduct" + str(self.id)

ORDER_STATUS = (
    ("Order Received" , "Order Received"),
    ("Order Processing" , "Order Processing"),
    ("Order on the Way" , "Order on the Way"),
    ("Order Completed" , "Order Completed"),
    ("Order Cancelled" , "Order Cancelled"),
)


def validate_Phone_Number(value , length = 10):
    if len(str(value)) != 10 :
        raise ValidationError("This is not a Valid Phone Number")

class Order(models.Model):
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    ordered_by = models.CharField(max_length=200)
    shipping_address = models.CharField(max_length=200)
    mobile = models.CharField(max_length=10 , validators=[validate_Phone_Number])
    email = models.EmailField(null=True, blank=True)
    subtotal = models.PositiveIntegerField()
    discount = models.PositiveIntegerField()
    total = models.PositiveIntegerField()
    order_status = models.CharField(max_length=50 , choices=ORDER_STATUS)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Order : " + str(self.id)


    

