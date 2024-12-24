from django.urls import path, include
from controller import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('groups', views.GroupViewSet)
router.register('permissions', views.PermissionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
