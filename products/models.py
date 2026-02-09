from django.db import models
import os
import datetime
from django.urls import reverse
from category.models import Category

# Create your models here.
def getFileName(request, filename):
  now_time = datetime.datetime.now().strftime("%Y%m%d%H:%M:%S")
  new_filename = "%s%s"%(now_time, filename)
  return os.path.join('uploads', new_filename)


class Product(models.Model):
    product_name    = models.CharField(max_length=100, unique=True)
    slug            = models.SlugField(unique=True, max_length=200)
    description     = models.TextField(max_length=500, blank=True)
    original_price  = models.IntegerField()
    offer_price     = models.IntegerField()
    main_image      = models.ImageField(upload_to=getFileName)
    image2          = models.ImageField(upload_to='products/', blank=True, null=True)
    is_available    = models.BooleanField(default=True)
    category        = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date    = models.DateTimeField(auto_now_add=True)
    modified_date   = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_name
    
    @property
    def price(self):
        return self.offer_price

    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])

class ProductVariation(models.Model):
    SIZE_CHOICES = (
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
        ('XXL', 'Double Extra Large'),

        # Pant sizes
        ('28', '28'),
        ('30', '30'),
        ('32', '32'),
        ('34', '34'),
        ('36', '36'),
        ('38', '38'),
        ('40', '40'),
        ('42', '42'),
        ('44', '44'),
    )

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variations')
    size    = models.CharField(max_length=5, choices=SIZE_CHOICES)
    stock   = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.product.product_name} - {self.size}"