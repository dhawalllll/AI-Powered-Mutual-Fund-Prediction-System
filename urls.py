from django.urls import path,include
from . import views


urlpatterns = [
        path('', views.navbar,name='navbar'),
        path('user_login/', views.user_login,name='user_login'),
        path('user_registration/', views.user_registration,name='user_registration'),
        path('admin_login/', views.admin_login,name='admin_login'),
        path('logout/', views.logout,name='logout'),
        path('admin_registration/', views.admin_registration,name='admin_registration'),
        path('admin_login/', views.admin_login,name='admin_login'),
        path('admin_logout/', views.admin_logout,name='admin_logout'),
        path('userhome/', views.userhome,name='userhome'),
        path('admin_home/', views.admin_home,name='admin_home'),
        path('user_contact/', views.user_contact,name='user_contact'),
        path('user_about/', views.user_about,name='user_about'),
        path('view_user/', views.view_user,name='view_user'),

        path('form/',views.input_form, name='form'),
        path('result/',views.result, name='result'),
        path('recommend/',views.recommend, name="/recommend"),


       


]