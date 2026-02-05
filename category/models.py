from django.db import models
import datetime
import os

# Create your models here.
def getFileName(filename):
    now_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    new_filename = f"{now_time}_{filename}"
    return os.path.join('categories', new_filename)

class Category(models.Model):
  category_name = models.CharField(max_length=100)
  slug = models.SlugField(unique=True, max_length=150, blank=True)
  image = models.ImageField(upload_to=getFileName, blank=True, null=True)  # ✅ Use function directly
  status = models.BooleanField(default=False)
  show_in_navbar = models.BooleanField(default=True)
  created_at = models.DateTimeField(auto_now_add=True)



  class Meta:
    verbose_name = 'category'
    verbose_name_plural = 'categories'

  def __str__(self):
    return self.category_name

