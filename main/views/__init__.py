from main.views.information import (
    InformationCreateAPIView, 
    InformationUpdateAPIView, 
    InformationDestroyAPIView, 
    InformationListAPIView, 
    InformationRetrieveAPIView,
    InformationLotinListAPIView,
    InformationLotinRetrieveAPIView
)
from main.views.cadre import CadreListAPIView, CadreCreateAPIView, CadreDeleteAPIView
from main.views.poster import PosterCreateAPIView, PosterDeleteAPIView
from main.views.serial import SerialListAPiView, SerialCreateAPIView, SerialUpdateAPIView, SerialRetrieveAPIView, SerialDestroyAPIView
from main.views.bookmark import BookmarkCreateAPIView, BookmarkListAPIView, BookmarkDestroyAPIView, BookmarkListIdAPIView
from main.views.rating import RatingCreateAPIView, RatingUpdateAPIView, RatingRetrieveAPIView
