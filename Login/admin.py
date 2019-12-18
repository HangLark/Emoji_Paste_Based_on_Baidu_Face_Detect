from django.contrib import admin

from django.contrib import admin
from . import models

admin.site.register(models.User)
admin.site.register(models.Images)
# Register your models here.
