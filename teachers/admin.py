from django.contrib import admin
from teachers.models import *

# Register your models here.
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Grade)
admin.site.register(Course)
admin.site.register(Student_Course)
