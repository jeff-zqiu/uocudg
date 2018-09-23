from django.contrib import admin
from django.contrib.auth.models import User as AuthUser
from .models import *


# Register your models here.

admin.site.register(Post)
admin.site.register(Comments)
admin.site.register(Profile)