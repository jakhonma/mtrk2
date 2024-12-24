from django.urls import path
from report import views

urlpatterns = [
    path('report-list/', views.ReportListAPIView.as_view()),
    path('report-create/', views.ReportCreateAPIView.as_view()),
    path('report-edit/<int:pk>/', views.ReportUpdateAPIView.as_view()),
    path('report-delete/<int:pk>/', views.ReportDeleteAPIView.as_view()),
    path('export-excel/', views.ExcelExportReportListAPIView.as_view()),
]
