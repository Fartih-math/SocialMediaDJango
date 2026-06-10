from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('profile/<int:user_id>/', views.profile_view, name='profile'),
    path('follow/<int:user_id>/', views.follow_user, name='follow'),
    path('like/<int:user_id>/', views.like_user, name='like_user'),
]
