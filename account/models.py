from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.urls import reverse
from datetime import datetime, date
from ckeditor.fields import RichTextField
from django.utils import timezone

from teachers.models import *

# Create your models here.


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_teacher = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

# Video models
    
class Posts(models.Model):
    id = models.AutoField(primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=255)
    #title_tag = models.CharField(max_length=255, default="The Education Today")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    #body = models.TextField()
    body = RichTextField(blank=True, null=True)
    post_date = models.DateTimeField(auto_now_add=True)
    snippet = models.CharField(max_length=255)

    file = models.FileField(null=True, blank=True, upload_to="documents/")
    #file = models.ManyToManyField('PostFile')
    #files = models.FileField(upload_to='post_files/')

    #objects = models.Manager()


    def __str__(self):
        return self.title + ' | ' + str(self.author)
    
    def get_absolute_url(self):
        #return reverse('article-detail', args=(str(self.id))) # type: ignore
        return reverse('posts')
    

class Replies(models.Model):
    post = models.ForeignKey(Posts, related_name="replies", on_delete=models.CASCADE)
    name = models.CharField(max_length=255, default="Unknown")
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.post.title, self.name)
    

