from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('', views.home, name='home'),
    path('login/', views.sigin, name='login'),
    path('logout/', views.signout, name='logout'),
    path('task/', views.task, name='tasks'),
    path('task/create/', views.task_create, name='create_task'),
    path('task/<int:task_id>/', views.task_detail, name='task_detail'),
]
