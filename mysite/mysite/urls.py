from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from users.models import Profile,FriendRequest
from rest_framework import serializers,viewsets,routers,status

##API PART##
class Profileserializer(serializers.ModelSerializer):
    class Meta:
        model=Profile
        fields="__all__"
from rest_framework import generics
class ProfileViewSet(viewsets.ModelViewSet):
    queryset=Profile.objects.all()
    serializer_class=Profileserializer

class Friend(serializers.ModelSerializer):
    class Meta:
        model=FriendRequest
        fields='__all__'

class FriendView(viewsets.ModelViewSet):
    queryset = FriendRequest.objects.all()
    serializer_class = Friend
router=routers.DefaultRouter()
router.register('profile',ProfileViewSet,basename='Profile')
router.register('friends',FriendView,)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('api/', include(router.urls),name='api'),

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
