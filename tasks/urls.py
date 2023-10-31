from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('', views.home, name='home'),
    path('login/', views.sigin, name='login'),
    path('logout/', views.signout, name='logout')
]
