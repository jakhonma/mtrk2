from django.contrib.auth import authenticate, login
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from authentication.models import User, AdminUser, UserRoles
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import Group, Permission


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True)

    class Meta:
        model = Group
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(read_only=True)
    class Meta:
        model = User
        fields = '__all__'


class UserResponsibleSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    full_name = serializers.CharField(max_length=200)



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
        user_role, created = UserRoles.objects.get_or_create(
            name="LOW_USER",  
        )
        user = User.objects.create(**validated_data)
        user.user_role = user_role
        user.save()
        return user
    
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


class PasswordChangeWithOldSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    old_password = serializers.CharField()
    new_password = serializers.CharField(min_length=8)

    def validate_user_id(self, value):
        if not User.objects.filter(id=value).exists():
            raise serializers.ValidationError("Foydalanuvchi topilmadi.")
        return value

    def validate(self, attrs):
        user_id = attrs.get('user_id')
        old_password = attrs.get('old_password')
        user = User.objects.get(id=user_id)

        # Eski passwordni tekshirish
        if not check_password(old_password, user.password):
            raise serializers.ValidationError({"msg": "Eski parol noto'g'ri."})
        return attrs

    def save(self):
        user_id = self.validated_data['user_id']
        new_password = self.validated_data['new_password']
        user = User.objects.get(id=user_id)
        user.set_password(new_password)
        user.save()
