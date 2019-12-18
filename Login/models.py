from django.db import models


class User(models.Model):
    ID = models.CharField("用户名", primary_key=True, max_length=15)
    password = models.CharField("密码", max_length=15)

    class Meta:
        db_table = 'User List'


class Images(models.Model):
    filename = models.CharField(primary_key=True, max_length=128)
    # flename = models.CharField(max_length=252, default="")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Image Owner")

    class Meta:
        db_table = 'Image List'
# Create your models here.
