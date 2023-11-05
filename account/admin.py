from django.contrib import admin

# Register your models here.

from .models import Posts, CustomUser2, Replies, Account

admin.site.register(Posts)
admin.site.register(CustomUser2)
admin.site.register(Replies)
admin.site.register(Account)



