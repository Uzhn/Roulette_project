from django.db import models

from users.models import CustomUser


class RouletteRound(models.Model):
    """Модель раунда рулетки."""
    is_active = models.BooleanField(default=True)


class CellInRound(models.Model):
    """Модель ячеек в раунде."""
    round = models.ForeignKey(RouletteRound, on_delete=models.CASCADE)
    cell = models.IntegerField()
    is_dropped = models.BooleanField(default=False)


class SpinLog(models.Model):
    """Модель лога вращения рулетки."""
    user = models.ForeignKey(CustomUser, related_name='user_in_round', on_delete=models.CASCADE)
    round = models.ForeignKey(RouletteRound,
                              related_name='log_round',
                              on_delete=models.CASCADE)
    number = models.IntegerField(null=True, blank=True)
    jackpot_dropped = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
