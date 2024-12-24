from django.urls import path, include
from letter import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('letter', views.LetterViewSet)
router.register('notice', views.NoticeViewSet)
router.register('sender', views.SenderViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
