from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import UserBlock
from .models import Block


@login_required(login_url='login')
def lessons_board_view(request):
    user = request.user
    users_progress = {}

    blocks = Block.objects.all()

    for block in blocks:
        try:
            user_block = UserBlock.objects.get(user=user, block = block)
            progress = user_block.completed_lessons / block.number_of_lessons * 100
            users_progress[block.id] = round(progress)
        except UserBlock.DoesNotExist:
            users_progress[block.id] = 0
        print(users_progress[block.id])


    return render(request, 'lessons/lesson_board.html',
                  {
                      'courses': blocks,
                      'progress': users_progress
                  })

@login_required(login_url='login')
def lesson_view(request):
    # logika ładowania pytań w lekcji
    return render(request, 'lessons/lesson_board.html', {})
