from django.core.exceptions import ValidationError


def validate_related_habit_and_reward(value):
    """
    Валидатор, исключающий одновременный выбор связанной привычки и указания вознаграждения.
    """
    if value.related_habit and value.reward:
        raise ValidationError(
            "Нельзя одновременно выбирать связанную привычку и указывать вознаграждение."
        )


def validate_execution_time(value):
    """
    Валидатор, проверяющий, что время выполнения не больше 120 секунд.
    """
    if value > 120:
        raise ValidationError("Время выполнения должно быть не больше 120 секунд.")


def validate_pleasant_habit(value):
    """
    Валидатор, проверяющий, что в связанные привычки могут попадать только привычки с признаком приятной привычки.
    """
    if value and not value.is_pleasant:
        raise ValidationError(
            "В связанные привычки могут попадать только привычки с признаком приятной привычки."
        )


def validate_reward_or_related_habit_for_pleasant(value):
    """
    Валидатор, проверяющий, что у приятной привычки не может быть вознаграждения или связанной привычки.
    """
    if value.is_pleasant and (value.reward or value.related_habit):
        raise ValidationError(
            "У приятной привычки не может быть вознаграждения или связанной привычки."
        )


def validate_periodicity(value):
    """
    Валидатор, проверяющий, что нельзя выполнять привычку реже, чем 1 раз в 7 дней.
    """
    if value < 1 or value > 7:
        raise ValidationError("Нельзя выполнять привычку реже, чем 1 раз в 7 дней.")