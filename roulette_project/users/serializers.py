from rest_framework import serializers

from .models import CustomUser


class AuthUserSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации нового пользователя."""

    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'username', 'password')

    def create(self, validated_data):
        """Метод создает пользователя и хэширует пароль."""
        user = CustomUser.objects.create(**validated_data)
        user.set_password(user.password)
        user.save()
        return user


class ActiveUsersSerializer(serializers.ModelSerializer):
    """Сериализатор самых активных пользователей."""
    user_id = serializers.IntegerField(source='id')
    count_of_rounds = serializers.IntegerField()
    avg_spins = serializers.DecimalField(max_digits=3, decimal_places=None)

    class Meta:
        model = CustomUser
        fields = ('user_id', 'count_of_rounds', 'avg_spins')

