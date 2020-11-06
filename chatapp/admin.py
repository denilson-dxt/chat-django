from django.contrib import admin
from .models import User, UserSystem, Test, Friend, SentRequest, ReceivedRequest
# Register your models here.
admin.site.register(User)
admin.site.register(UserSystem)

admin.site.register(Friend)
admin.site.register(SentRequest)
admin.site.register(ReceivedRequest)



