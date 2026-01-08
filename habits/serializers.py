from rest_framework import serializers

from .models import Habit


class HabitSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Habit.
    """

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Habit
        fields = "__all__"
        read_only_fields = ["user"]  # Пользователь не может менять поле user

    def validate(self, data):
        """
        Дополнительная валидация данных.
        """
        related_habit = data.get("related_habit")
        reward = data.get("reward")
        is_pleasant = data.get("is_pleasant")

        if related_habit and reward:
            raise serializers.ValidationError(
                "Нельзя одновременно выбирать связанную привычку и указывать вознаграждение."
            )
        if is_pleasant and (reward or related_habit):
            raise serializers.ValidationError(
                "У приятной привычки не может быть вознаграждения или связанной привычки."
            )
        if related_habit and not related_habit.is_pleasant:
            raise serializers.ValidationError(
                "В связанные привычки могут попадать только привычки с признаком приятной привычки."
            )
        return data
