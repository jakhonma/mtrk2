from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView

from authentication import views

router = routers.DefaultRouter()
router.register('users', views.UserViewSet, basename='users')

urlpatterns = [
    path('register/', views.RegisterAPIView.as_view(), name='register'),
    path('login/', views.LoginAPIView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/', views.AuthenticationUser.as_view(), name='user'),
    path('user-bookmark-delete/', views.UserBookMarkClearView.as_view(), name='user-bookmark-delete'),
    path('password-change-with-old/', views.PasswordChangeWithOldView.as_view(), name='password-change-with-old'),
    path('user-notification-count/', views.UserNotificationAPIView.as_view()),
    path('', include(router.urls)),
]
