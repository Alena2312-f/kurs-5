from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied

from .models import Habit
from .serializers import HabitSerializer


class HabitCreateAPIView(generics.CreateAPIView):
    """
    Представление для создания привычки.
    """

    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated]


class HabitListAPIView(generics.ListAPIView):
    """
    Представление для просмотра списка привычек текущего пользователя.
    """

    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Возвращает только привычки текущего пользователя.
        """
        return Habit.objects.filter(user=self.request.user).order_by("id")


class HabitPublicListAPIView(generics.ListAPIView):
    """
    Представление для просмотра списка публичных привычек.
    """

    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Возвращает только публичные привычки.
        """
        return Habit.objects.filter(is_public=True)


class HabitRetrieveAPIView(generics.RetrieveAPIView):
    """
    Представление для просмотра информации о привычке.
    """

    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Habit.objects.all()

    def get_object(self):
        """
        Возвращает объект, только если он принадлежит текущему пользователю.
        """
        obj = super().get_object()
        if obj.user != self.request.user:
            raise PermissionDenied("У вас нет прав на просмотр этой привычки.")
        return obj


class HabitUpdateAPIView(generics.UpdateAPIView):
    """
    Представление для редактирования привычки.
    """

    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Habit.objects.all()

    def get_object(self):
        """
        Возвращает объект, только если он принадлежит текущему пользователю.
        """
        obj = super().get_object()
        if obj.user != self.request.user:
            raise PermissionDenied("У вас нет прав на редактирование этой привычки.")
        return obj


class HabitDestroyAPIView(generics.DestroyAPIView):
    """
    Представление для удаления привычки.
    """

    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Habit.objects.all()

    def get_object(self):
        """
        Возвращает объект, только если он принадлежит текущему пользователю.
        """
        obj = super().get_object()
        if obj.user != self.request.user:
            raise PermissionDenied("У вас нет прав на удаление этой привычки.")
        return obj


from django.shortcuts import render

# Create your views here.
