from django.db import models
from django.utils import timezone
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name


class Post(models.Model):
    img = models.ImageField(upload_to='upload/image/', default=0)
    title = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=0)
    created_date = models.DateTimeField(default=timezone.now)
    desc = models.TextField()

