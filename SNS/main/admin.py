from django.contrib import admin
from .models import Message,Comment#,Follow

admin.site.register(Comment)
admin.site.register(Message)
#admin.site.register(Follow)
