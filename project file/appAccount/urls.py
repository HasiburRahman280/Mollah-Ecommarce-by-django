from django.contrib import admin
from django.urls import path
from .  import views
urlpatterns = [

    path('signup/',views.auth_signup, name='signup'),
    path('login/',views.auth_login, name='login'),
    path('logout/',views.auth_logout, name='logout'),

    path('user-profile-view/',views.user_profile_view, name='user_profile_view'),
    path('user-profile-edit/',views.user_profile_edit, name='user_profile_edit'),
    path('user-profile-pic/',views.profile_picture, name='profile_picture'),
    path('update-profile-pic/',views.update_Profile_Pic, name='update_Profile_Pic'),

]