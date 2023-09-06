import random

from django.db import transaction

from .models import CellInRound, RouletteRound, SpinLog


def spin_roulette(user_id):
    """Функция вращения рулетки."""
    try:
        with transaction.atomic():
            roulette_round = RouletteRound.objects.filter(is_active=True).first()

            if not roulette_round:
                roulette_round = RouletteRound.objects.create()
                cell_numbers = [x for x in range(1, 11)]
                random.shuffle(cell_numbers)
                for cell_number in cell_numbers:
                    CellInRound.objects.create(round=roulette_round, cell=cell_number)

            available_cells = CellInRound.objects.filter(round=roulette_round, is_dropped=False)

            if available_cells.exists():
                result_cell = random.choice(available_cells)
                result_number = result_cell.cell
                result_cell.is_dropped = True
                result_cell.save()
                SpinLog.objects.create(user=user_id, round=roulette_round, number=result_number)
                return result_number
            roulette_round.is_active = False
            roulette_round.save()
            SpinLog.objects.create(user=user_id, round=roulette_round, jackpot_dropped=True)
            CellInRound.objects.all().delete()
            return 'Джекпот!'

    except Exception as err:
        return str(err)
