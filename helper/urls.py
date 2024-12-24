from django.urls import path, include
from rest_framework import routers
from helper import views

router = routers.DefaultRouter()
router.register('department', views.DepartmentViewSet)
router.register('fond', views.FondViewSet)
router.register('category', views.CategoryViewSet)
router.register('mtv', views.MTVViewSet)
router.register('format', views.FormatViewSet)
router.register('language', views.LanguageViewSet)
router.register('region', views.RegionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('category-view/', views.CategoryListView.as_view()),

    # Information kiritayotganda Helper Filter
    path('department-fond/<int:department_id>/', views.FontListDepartmentAPIView.as_view()),
    path('fond-category/<int:fond_id>/', views.CategoryFondListView.as_view()),
    path('category-parent/<int:category_id>/', views.ParentCategoryListView.as_view()),

    # Mtv, Region, Language va Format List
    path('helper-list-view/', views.HelperListView.as_view()),

    # Filter
    path('fond-id-list-category/', views.CategoryFondIdListView.as_view()),
    path('category-parent-id-list/', views.CategoryParenIdListView.as_view()),
]
