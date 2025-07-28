from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from .models import Lesson, UserLesson, UserBlock, Block, Question


@login_required(login_url='login')
def blocks_board_view(request):
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
def lessons_board_view(request, block_id):
    user = request.user
    users_progress = {}

    lessons = Lesson.objects.all().filter(block_id=block_id)

    for lesson in lessons:
        try:
            user_lesson = UserLesson.objects.get(user=user, lesson=lesson)
            users_progress[lesson.id] = user_lesson.result
        except UserLesson.DoesNotExist:
            users_progress[lesson.id] = 0

    return render(request, 'lessons/lesson_board.html', {
        'courses': lessons,
        'progress': users_progress
    })

@login_required(login_url='login')
def lesson_view(request, block_id, lesson_id):
    lesson = Lesson.objects.get(id = lesson_id)
    questions = lesson.question_set.all()
    questions_list = list(questions.values_list('id', flat = True))
    questions_dict = {question.id:question for question in questions}


    return render(request, 'lessons/lesson_view.html', { 'lesson': lesson,
                                # 'questions': questions,
                                'questions_list': questions_list,
                                'questions_dict': questions_dict,
                                 })

def check_answer_ajax(request):
    if request.method == 'POST':
        question_id = request.POST.get('question_id')
        user_answer = request.POST.get('user_answer')

        question = get_object_or_404(Question, id=question_id)

        result = check_answer(question, user_answer)

        return JsonResponse(result)
    return JsonResponse({'error': 'Invalid request'}, status=400)

def check_answer(question, user_answer):
    if question.question_type == 'W':
        is_correct = user_answer.lower().strip() == question.correct_answer.lower().strip()
    else:
        is_correct = user_answer == question.correct_answer


    return {"correct": is_correct, "correct-answer": question.correct_answer}