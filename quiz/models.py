from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.urls import reverse


class UserInfo(models.Model):
    #user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=20, unique=True, null=True)
    userid = models.CharField(max_length=20, unique=True, null=True)
    userpw = models.CharField(max_length=20, unique=True, null=True)
    score = models.IntegerField(default=0)
    rank = models.IntegerField(default=0)

    # USERNAME_FIELD = 'userid'
    # REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['score']


class Category(models.Model):
    name = models.CharField(max_length=20)

    @staticmethod
    def get_all_categories():
        return Category.objects.all()

    def __str__(self):
        return self.name


class Choice(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=30, null=True)
    option1 = models.CharField(max_length=30, null=True)
    option2 = models.CharField(max_length=30, null=True)
    option3 = models.CharField(max_length=30, null=True)
    option4 = models.CharField(max_length=30, null=True)
    answer = models.CharField(max_length=30, null=True)
    hint = models.CharField(max_length=50, null=True)
    score = models.IntegerField(default=0)



    @staticmethod
    def get_all_products():
        return Choice.objects.all()

    @staticmethod
    def get_all_products_by_categoryid(category_id):
        if category_id:
            return Choice.objects.filter(category = category_id)
        else:
            return Choice.get_all_products();

    def __str__(self):
        return self.title
