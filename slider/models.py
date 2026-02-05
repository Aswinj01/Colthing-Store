from django.db import models

# Create your models here.
class Slider(models.Model):
    title = models.CharField(max_length=150, blank=True)
    image = models.ImageField(upload_to='sliders/')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title if self.title else "Slider Image"

