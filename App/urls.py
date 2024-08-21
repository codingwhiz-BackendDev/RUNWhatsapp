from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name = 'index'),
    path('login', views.login, name = 'login'),
    path('register', views.register, name = 'register'),
    path('add_contact', views.add_contact, name = 'add_contact'), 
    path('status', views.status, name = 'status'),
    path('chat/<str:pk>', views.chat, name = 'chat'),
    path('settings', views.settings, name = 'settings'),
    path('logout', views.logout, name = 'logout'),
    path('write_status', views.write_status, name = 'write_status'),
    path("post_status", views.post_status, name='post_status'),
    path("send_message", views.send_message, name='send_message'),
    path("contact_profile/<str:pk>", views.contact_profile, name='contact_profile'),
    path("get_chat_message/<str:pk>", views.get_chat_message, name='get_chat_message'), 
    path('delete_post/<str:pk>', views.delete_post, name='delete_post'),
    path('group_chat_comment', views.group_chat_comment, name='group_chat_comment'),
    path('communities', views.communities, name='communities'),
    path('view_community/<str:pk>', views.view_community, name='view_community'),
]
