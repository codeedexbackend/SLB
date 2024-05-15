from django.urls import path
from backend import views





urlpatterns = [
    path('register/', views.UserRegistrationAPIView.as_view(), name='user-registration'),
    path('profile-update/', views.UserProfileUpdateAPIView.as_view(), name='profile-update'),
    path('login/', views.LoginAPIView.as_view(), name='login'),
]
