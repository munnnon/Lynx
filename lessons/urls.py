from django.urls import path
from . import views

urlpatterns = [
    path('', views.lessons_board_view, name='lessons_board_view'),
    path('/<int:id>', views.lesson_view, name='lesson_view')
]
