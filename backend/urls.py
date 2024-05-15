from django.urls import path
from backend import views





urlpatterns = [
    path('register/', views.UserRegistrationAPIView.as_view(), name='user-registration'),
    path('profile-update/<int:user_id>/', views.UserProfileUpdateAPIView.as_view(), name='profile-update-by-user-id'),
    path('login/', views.LoginAPIView.as_view(), name='login'),
    path('crews/', views.CrewListAPIView.as_view(), name='crew-list'),
    path('crews/<int:crew_id>/designations/', views.DesignationListByCrewAPIView.as_view(), name='designation-list-by-crew'),
    path('crews-create/', views.CrewCreateAPIView.as_view(), name='crew-create'),
    path('crews/<int:crew_id>/designations-create/', views.DesignationCreateAPIView.as_view(), name='designation-create-by-crew'),
    path('crews/<int:id>/', views.CrewDetailAPIView.as_view(), name='crew-detail'),
    path('crews-name/<str:name>/', views.CrewDetailByNameAPIView.as_view(), name='crew-detail-by-name'),


]
