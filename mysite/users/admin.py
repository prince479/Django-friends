from django.contrib import admin
from .models import Address,Signup,FriendRequest,Profile
# Register your models here.
admin.site.register(Signup)
admin.site.register(Profile)
admin.site.register(FriendRequest)
admin.site.register(Address)
