from django.conf import settings
from django.db import models
from products.models import Product
import uuid
import datetime


class Order(models.Model):

    #New Unique Order ID
    order_id = models.CharField(max_length=20, unique=True, editable=False, blank=True)
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()

    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)

    total_price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    # Auto Generate Order ID
    def save(self, *args, **kwargs):
        if not self.order_id:
            self.order_id = self.generate_order_id()
        super().save(*args, **kwargs)

    def generate_order_id(self):
        date_str = datetime.datetime.now().strftime("%Y%m%d")
        random_str = uuid.uuid4().hex[:4].upper()
        return f"ORD{date_str}{random_str}"

    def __str__(self):
        return self.order_id


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.CharField(max_length=10)
    price = models.IntegerField()
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.product.product_name} - {self.size}"