from django.urls import path, include
from letter import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('sender', views.SenderViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('user-notification-list/', views.UserNotificationListAPIView.as_view()),

    path('letter-create/', views.LetterCreateAPIView.as_view()),

    path('user-letter-progress-approved/', views.LetterProgressCreateApprovedAPIView.as_view()),
    path('user-letter-progress-rejected/', views.LetterProgressCreateRejectedAPIView.as_view()),

    path('user-letter-progress-all/', views.LetterProgressUserAllAPIView.as_view()),
    path('user-letter-progress-send/', views.LetterProgressUserSentAPIView.as_view()),
    path('user-letter-progress-recipient/', views.LetterProgressUserRecipientAPIView.as_view())
]
