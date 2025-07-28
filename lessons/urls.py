from django.urls import path
from . import views

urlpatterns = [
    path('', views.blocks_board_view, name='blocks_board_view'),
    path('<int:block_id>/', views.lessons_board_view, name='lessons_board_view'),
    path('<int:block_id>/<int:lesson_id>', views.lesson_view, name='lesson_view'),
    path('check-answer/', views.check_answer_ajax, name='check_answer_ajax'),
]
