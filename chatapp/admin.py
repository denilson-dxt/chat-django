from django.contrib import admin
from .models import User, UserSystem

# Register your models here.
admin.site.register(User)
admin.site.register(UserSystem)