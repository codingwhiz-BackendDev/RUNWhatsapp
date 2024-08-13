from django.contrib import admin
from .models import myContact, Profile, Status, Message, Communities


admin.site.register(myContact)
admin.site.register(Profile)
admin.site.register(Status)
admin.site.register(Message)
admin.site.register(Communities)
