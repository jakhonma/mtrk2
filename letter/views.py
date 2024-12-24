from rest_framework import viewsets, views, generics, response

from letter.models import Sender, Notice, Letter
from letter.serializers import SenderSerializer, NoticeSerializer, LetterSerializer


class SenderViewSet(viewsets.ModelViewSet):
    queryset = Sender.objects.all()
    serializer_class = SenderSerializer


class NoticeViewSet(viewsets.ModelViewSet):
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer


class LetterViewSet(viewsets.ModelViewSet):
    queryset = Letter.objects.all()
    serializer_class = LetterSerializer
