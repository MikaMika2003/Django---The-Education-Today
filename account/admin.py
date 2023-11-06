from django.contrib import admin

# Register your models here.

from .models import Posts, Replies, Account

admin.site.register(Posts)
admin.site.register(Replies)
admin.site.register(Account)



