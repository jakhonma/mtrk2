from django.urls import path, include
from letter import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('sender', views.SenderViewSet)

urlpatterns = [
    path('', include(router.urls)),

    path('letter-create/', views.LetterCreateAPIView.as_view()),
    path('user-notification-list/', views.UserNotificationListAPIView.as_view()),


    path('user-letter-progress-list/', views.LetterProgressAPIView.as_view()),
]
