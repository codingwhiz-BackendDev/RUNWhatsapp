from django.contrib import admin
from .models import myContact, Profile, Status, Message, Communities,Group_comment



admin.site.register(Profile)
admin.site.register(Status)
admin.site.register(Message)
admin.site.register(Communities)
admin.site.register(Group_comment)


class myContactAdmin(admin.ModelAdmin):
    list_display = ('user', 'contact', 'user_phone_number', 'phone_number')

admin.site.register(myContact, myContactAdmin)