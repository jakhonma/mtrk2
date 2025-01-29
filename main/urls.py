from django.urls import path, include
from main import views

urlpatterns = [
    # Information
    path('information/', views.InformationListAPIView.as_view()),
    path('information-lotin/', views.InformationLotinListAPIView.as_view()),
    path('information/<int:pk>/', views.InformationRetrieveAPIView.as_view()),
    path('information-lotin/<int:pk>/', views.InformationLotinRetrieveAPIView.as_view()),
    path('create-information/', views.InformationCreateAPIView.as_view()),
    path('edit-information/<int:pk>/', views.InformationUpdateAPIView.as_view()),
    path('delete-information/<int:pk>/', views.InformationDestroyAPIView.as_view()),

    # Poster
    path('information/<int:information_id>/create-poster/', views.PosterCreateAPIView.as_view()),
    path('information/<int:information_id>/delete-poster/<int:pk>/', views.PosterDeleteAPIView.as_view()),

    # Cadre
    path('information/<int:information_id>/list-cadre/', views.CadreListAPIView.as_view()), #Informationga tegishli Cadrelar list
    path('information/<int:information_id>/create-cadre/', views.CadreCreateAPIView.as_view()), #Informationga tegishli Cadrelar qo'shish
    path('information/<int:information_id>/delete-cadre/<int:pk>/', views.CadreDeleteAPIView.as_view()), #Informationga tegishli Cadrelar o'chirish

    # Serial
    path('information/<int:information_id>/list-serial/', views.SerialListAPiView.as_view()), #Informationga tegishli Seriallar listi
    path('information/<int:information_id>/one-serial/<int:pk>/', views.SerialRetrieveAPIView.as_view()), #Informationga tegishli Seriallar bittasini olish
    path('information/<int:information_id>/create-serial/', views.SerialCreateAPIView.as_view()), #Informationga tegishli Seriallar qo'shish
    path('information/<int:information_id>/edit-serial/<int:pk>/', views.SerialUpdateAPIView.as_view()), #Informationga tegishli Seriallar o'zgartirish
    path('information/<int:information_id>/delete-serial/<int:pk>/', views.SerialDestroyAPIView.as_view()), #Informationga tegishli Seriallar o'zgartirish

    # bookmark
    path('bookmark/list/', views.BookmarkListAPIView.as_view()),
    path('bookmark/list-id/', views.BookmarkListIdAPIView.as_view()),
    path('bookmark/create/', views.BookmarkCreateAPIView.as_view()),
    path('<int:information_id>/bookmark/delete/', views.BookmarkDestroyAPIView.as_view()),

    # rating
    path('<int:information_id>/rating-get/', views.RatingRetrieveAPIView.as_view()),
    path('<int:information_id>/rating-create/', views.RatingCreateAPIView.as_view()),
    path('<int:information_id>/rating-update/<int:pk>/', views.RatingUpdateAPIView.as_view()),
]
