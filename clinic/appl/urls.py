from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns=[path('register/', views.register, name="registration"),
             path('login/', views.user_login, name='login'),
             path('add_visit/', views.add_visit, name="add_visit"),
             path('', views.home ,name="home"),
             path('logout/', LogoutView.as_view(), name='logout'),
             path('prescription/<int:id>/', views.prescription, name="prescription"),

             ]