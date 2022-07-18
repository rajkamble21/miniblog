from django.db import models

# Create your models here.
class Post(models.Model):
    img = models.ImageField(upload_to='upload/image/', default=0)
    title = models.CharField(max_length=50)
    desc = models.TextField()