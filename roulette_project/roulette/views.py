from django.db.models import Avg, Count, F
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import CustomUser
from users.serializers import ActiveUsersSerializer

from .models import RouletteRound, SpinLog
from .serializers import RouletteStatisticsSerializer
from .utils import spin_roulette


class SpinRouletteView(APIView):
    """Вьюкласс для выполнения вращения рулетки."""

    def post(self, request):
        user_id = self.request.user
        try:
            result = spin_roulette(user_id)
            response_data = {
                "message": f"Рулетка вращена, выпала ячейка: {result}",
                "result": result,
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as err:
            return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)


class RouletteStatisticsView(generics.ListAPIView):
    """Вьюкласс для вывода статистики раундов рулетки."""
    serializer_class = RouletteStatisticsSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        queryset = RouletteRound.objects.annotate(
            count_of_users=Count('log_round__user', distinct=True)
        ).values('id', 'count_of_users')
        return queryset

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response({'statistics': serializer.data}, status=status.HTTP_200_OK)
        except Exception as err:
            return Response({'error': str(err)}, status=status.HTTP_400_BAD_REQUEST)


class ActiveUsersView(generics.ListAPIView):
    """Вьюкласс для вывода самых активных пользователей."""
    serializer_class = ActiveUsersSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        queryset = CustomUser.objects.annotate(
            count_of_rounds=Count('user_in_round__round', distinct=True),
            total_spins=Count('user_in_round__round'),
            avg_spins=F('total_spins') / F('count_of_rounds')
        ).values('id', 'count_of_rounds', 'avg_spins').filter(count_of_rounds__gt=0)
        return queryset.order_by('-avg_spins')

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response({'active_users': serializer.data}, status=status.HTTP_200_OK)
        except Exception as err:
            return Response({'error': str(err)}, status=status.HTTP_400_BAD_REQUEST)
