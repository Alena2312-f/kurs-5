from django.urls import path

from . import views

app_name = "habits"

urlpatterns = [
    path("create/", views.HabitCreateAPIView.as_view(), name="habit_create"),
    path("list/", views.HabitListAPIView.as_view(), name="habit_list"),
    path("public/", views.HabitPublicListAPIView.as_view(), name="habit_public_list"),
    path("<int:pk>/", views.HabitRetrieveAPIView.as_view(), name="habit_retrieve"),
    path("<int:pk>/update/", views.HabitUpdateAPIView.as_view(), name="habit_update"),
    path("<int:pk>/delete/", views.HabitDestroyAPIView.as_view(), name="habit_delete"),
]
