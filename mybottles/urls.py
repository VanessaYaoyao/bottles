from django.urls import path
from . import views

urlpatterns = [
    path('index/',views.index,name='index'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('personal_center/',views.personal_center,name='personal_center'),
    path('salvage/',views.salvage,name='salvage'),
    path('register/', views.register, name='register'),
    path('forget_password/', views.forget_password, name='forget_password'),
    path('change_password/', views.change_password, name='change_password'),
    path('edit_information/',views.edit_information,name='edit_information'),
    path('throw_one/',views.throw_one,name='throw_one'),
    path('find_one/', views.find_one, name='find_one'),
    path('mybottles/',views.mybottles,name='mybottle'),
    path('activate/<str:code>/', views.activate, name='activate'),
    path('reset_password/<str:code>/', views.reset_password, name='reset_password'),
    path('mybottles/bottle_delete/<int:id>',views.bottle_delete, name='bottle_delete'),
    path('mybottles/its_profile/<str:username>',views.its_profile, name='its_profile'),
]
