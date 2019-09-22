from django.urls import path
from .views import index,signup,home,login,logout,profile,profile_view,send_friend_request,accept_friend_request,cancel_friend_request,ignore_friend_request,edit_profile
urlpatterns = [

    path('',index,name='index'),
    path('signup/',signup,name='signup'),
    path('homepage/',home,name='homepage'),
    path('login/',login,name='login'),
    path('logout/',logout,name='logout'),
    path('myprofile',profile,name='myprofile'),
    path('view/<int:id>/',profile_view,name='view'),
    path('editprofile/',edit_profile,name='edit'),
    path('friend_request/send/<int:id>/',send_friend_request,name='send'),
    path('friend_request/accept/<int:id>/',accept_friend_request,name='accept'),
    path('friend_request/cancel/<int:id>/',cancel_friend_request,name='cancel'),
    path('friend_request/ignore/<int:id>/',ignore_friend_request,name='ignore'),

]
