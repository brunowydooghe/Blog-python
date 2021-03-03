from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField
# Create your models here.
STATUS = (
    (0, "Draft"),
    (1, "Publish")
)
class Category(models.Model):


    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('home')




class Post(models.Model):
    title = models.CharField(max_length=255, unique=True)
    image = models.ImageField(null=True, blank=True, upload_to="image/")
    slug = models.SlugField(max_length=255, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_post')
    keywords = models.TextField()
    created_on = models.DateField(auto_now_add=True)
    updated_on = models.DateField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    status = models.IntegerField(choices=STATUS, default=0)
    #keywords = RichTextField(blank=True, null=True)
    content = RichTextField(blank=True, null=True)



    class Meta:
        ordering = ['-created_on']
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('home')