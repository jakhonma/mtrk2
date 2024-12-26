from rest_framework import views, generics, response, status, permissions
from letter.serializers import NotificationSerializer
from letter.models import Notification


class UserNotificationListAPIView(generics.ListAPIView):
    """
        List a queryset.
    """
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = NotificationSerializer

    def list(self, request, *args, **kwargs):
        user = request.user
        queryset = Notification.objects.filter(recipient=user, is_read=False)
        serializer = self.get_serializer(queryset, many=True)
        data = {
            "count": queryset.count(),
            'notification': serializer.data
        }
        return response.Response(data=data)
