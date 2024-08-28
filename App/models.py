from django.db import models 
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from datetime import datetime

User = get_user_model()

class myContact(models.Model):
    contact = models.CharField(max_length=255, null=True)
    user = models.CharField(max_length=255, null=True)
    phone_number = models.CharField(max_length=255, null=True)
    user_phone_number = models.CharField(max_length=255, null=True)
    image = models.ImageField(upload_to='Profile Image', default='blank.png')
    user_image = models.ImageField(upload_to='Profile Image', default='blank.png')
    bio = models.CharField(max_length=255, null=True)
    last_message = models.CharField(max_length=255, default='No messages')
    
    def __str__(self):
        return str(self.contact)
    
class Profile(models.Model):
    image = models.ImageField(upload_to='Profile Image', default='blank.png')
    first_name = models.CharField(max_length=255, null=True,)
    username = models.ForeignKey(User,on_delete=models.CASCADE, null=True)
    bio = models.TextField()
    last_activity = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.username)
    
class Status(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to='Status', null= True)
    video = models.FileField(upload_to='Status', null= True)
    time = models.DateTimeField(auto_now_add=True)
    
    
class UserStatus(models.Model):
    user =  models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    status = models.ForeignKey(Status,on_delete=models.CASCADE)
     
    def __str__(self):
        return str(self.user)
    
class Message(models.Model):
    sender = models.CharField(max_length=255, null=True)
    receiver = models.CharField(max_length=255, null=True) 
    receiverId = models.CharField(max_length=255, null=True)
    senderId = models.CharField(max_length=255, null=True)
    message = models.CharField(max_length=255, null=True)
    def __str__(self):
        return str(self.message)
    

class Communities(models.Model):
    group_name = models.ForeignKey(Group, on_delete=models.CASCADE)
    group_admin = models.CharField(max_length=255, null=True)
    group_pic = models.ImageField(upload_to='Group image', default='blank.png')
    group_members = models.IntegerField(null=True)
    
    def __str__(self):
        return str(self.group_name)

class Group_comment(models.Model):
    sender = models.CharField(max_length=50000000, null=True) 
    comment =  models.CharField(max_length=50000000, null=True)
    userId = models.CharField(max_length=50, null=True) 
    profileimage = models.ImageField(default='blank.png')
    group_name = models.CharField(max_length=50000000, null=True)
    
    def __str__(self):
        return str(self.comment)