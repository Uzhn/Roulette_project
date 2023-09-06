from django.urls import path

from .views import ActiveUsersView, RouletteStatisticsView, SpinRouletteView

urlpatterns = [
    path('spin_roulette/', SpinRouletteView.as_view()),
    path('statistic/', RouletteStatisticsView.as_view()),
    path('active_users/', ActiveUsersView.as_view()),
]
