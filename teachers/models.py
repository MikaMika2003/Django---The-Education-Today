from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.urls import reverse
from datetime import datetime, date
from ckeditor.fields import RichTextField
from django.utils import timezone

# Create your models here.

class Course(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=120)
    subject_name = models.CharField(max_length=255, default="Intro to Art History") 
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    points = models.PositiveIntegerField(default=0)
    #semester = models.CharField(max_length=20, default="Fall 2023")

    def __str__(self):
        return self.name 

class Student_Course(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

class Quiz(models.Model):
    id = models.AutoField(primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, default=1)
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    weight = models.IntegerField(default=100)

    def __str__(self):
        return self.title

    
class Question(models.Model):
    id = models.AutoField(primary_key=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200,null=True)
    op1 = models.CharField(max_length=200,null=True)
    op2 = models.CharField(max_length=200,null=True)
    op3 = models.CharField(max_length=200,null=True)
    op4 = models.CharField(max_length=200,null=True)
    ans = models.IntegerField(choices=[(1, 'Option 1'), (2, 'Option 2'), (3, 'Option 3'), (4, 'Option 4')])
    points = models.IntegerField(default=1)

    
    def __str__(self):
        return self.quiz.title
    
class Grade(models.Model):
    id = models.AutoField(primary_key=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    grade = models.DecimalField(max_digits=5, decimal_places=2)
    user_score = models.PositiveIntegerField(default=0)
    max_score = models.PositiveIntegerField(default=1)
    attempts = models.PositiveIntegerField(default=0)
    date_added = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.quiz.title
    

