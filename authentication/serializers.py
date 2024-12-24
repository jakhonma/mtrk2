from django.contrib.auth import authenticate, login
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from authentication.models import User, AdminUser, LeaderUser, EmployeeUser
from django.utils.translation import gettext_lazy as _
from controller.serializers import GroupSerializer


class UserSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(read_only=True)
    class Meta:
        model = User
        fields = '__all__'


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    token_class = RefreshToken

    default_error_messages = {
        "no_active_account": _("No active account found with the given credentials")
    }

    def validate(self, attrs):
        authenticate_kwargs = {
            "username": attrs["username"],
            "password": attrs["password"],
        }
        try:
            authenticate_kwargs["request"] = self.context["request"]
        except KeyError:
            pass

        user = authenticate(**authenticate_kwargs)

        if user is None:
            raise ValidationError("Username yoki Password xato")

        login(authenticate_kwargs["request"], user)
        refresh = self.get_token(user)

        attrs["refresh"] = str(refresh)
        attrs["access"] = str(refresh.access_token)

        del attrs["password"], attrs["username"]

        return attrs

    @classmethod
    def get_token(cls, user):
        return cls.token_class.for_user(user)


class UserRegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=128)
    full_name = serializers.CharField(max_length=200)

    def create(self, validated_data):
        return User.objects.create(**validated_data)
    
    def get_tokens(self, user: User):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
    
    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")
        exist = User.objects.filter(username=username).exists()
        if exist:
            raise ValidationError(_(f"Tizimda {username} nomli username mavjud!"))
        if len(password) < 8:
            raise ValidationError(_("Password kamida 8 ta belgidan iborat bo'lishi kerak"))
        return attrs
