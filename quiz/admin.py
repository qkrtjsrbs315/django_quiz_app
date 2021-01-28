from django.contrib import admin

# Register your models here.
from quiz.models import UserInfo,Choice,Category

admin.site.register(UserInfo)
admin.site.register(Choice)
admin.site.register(Category)