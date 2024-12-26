from rest_framework import viewsets, generics, response, status, views, permissions
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from authentication.models import User
from authentication.serializers import UserSerializer, LoginSerializer, UserRegisterSerializer, PasswordChangeWithOldSerializer
from django.db import transaction
from letter.models import Notification


class LoginAPIView(generics.GenericAPIView):
    authentication_classes = []
    permission_classes = []

    def get_queryset(self):
        queryset = User.objects.all()
        return queryset

    def get_serializer_class(self):
        serializer = LoginSerializer
        return serializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return response.Response(
            serializer.validated_data,
            status=status.HTTP_200_OK
        )


class AuthenticationUser(views.APIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = UserSerializer(user)
        return response.Response(serializer.data)


class RegisterAPIView(generics.GenericAPIView):
    authentication_classes = []
    permission_classes = []

    def get_queryset(self):
        queryset = User.objects.all()
        return queryset

    def get_serializer_class(self):
        serializer = UserRegisterSerializer
        return serializer

    def post(self, request, *args, **kwargs):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        tokens = serializer.get_tokens(user)
        # tokens['username'] = user.username
        return response.Response(
            data=tokens, 
            status=status.HTTP_201_CREATED
        )


class UserViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        queryset = User.objects.filter(is_active=True)
        return queryset

    def get_serializer_class(self):
        return UserSerializer


class UserBookMarkClearView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        user = request.user.bookmarks.all()
        if not user.exists():
            return response.Response(status=status.HTTP_404_NOT_FOUND)
        with transaction.atomic():
            user.delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)


class PasswordChangeWithOldView(generics.CreateAPIView):
    """
        Create a model instance.
    """
    def create(self, request, *args, **kwargs):
        serializer = PasswordChangeWithOldSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            serializer.save()
        headers = self.get_success_headers(serializer.data)
        return response.Response({"message": "Parol muvaffaqiyatli o'zgartirildi."}, status=status.HTTP_201_CREATED, headers=headers)


class UserNotificationAPIView(generics.ListAPIView):
    """
    List a queryset.
    """
    def list(self, request, *args, **kwargs):
        count = Notification.objects.filter(recipient=request.user, is_read=False).count()
        data = {
            'count': count
        }
        return response.Response(data=data)
