from django.urls import path
from . import views

urlpatterns = [
    path('', views.msg_list, name='msg_list'),
    path('post', views.post_page, name='post_page'),
    path('msg_post', views.msg_post, name='msg_post'),
    path('my_page', views.my_page, name='my_page'),
    path('post_likes/<int:pk>/',views.get_likes,name='post_likes'),
]
