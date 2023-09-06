from rest_framework import serializers

from .models import RouletteRound


class RouletteStatisticsSerializer(serializers.ModelSerializer):
    """Сериализатор для статистики раундов рулетки."""
    round = serializers.IntegerField(source='id')
    count_of_users = serializers.IntegerField()

    class Meta:
        model = RouletteRound
        fields = ('round', 'count_of_users')
