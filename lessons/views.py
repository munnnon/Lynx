import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from accounts.views import update_streak
from .models import Lesson, UserLesson, UserBlock, Block, Question, UsersAnswers


@login_required(login_url='login')
def blocks_board_view(request):
    """
    Display all blocks with user's progress for each block.

    Args:
        request (HttpRequest): Incoming HTTP request.

    Returns:
        HttpResponse: Renders 'lesson_board.html' with all blocks and user's completion percentage.
    """
    user = request.user
    users_progress = {}

    blocks = Block.objects.all()

    for block in blocks:
        try:
            user_block = UserBlock.objects.get(user=user, block = block)
            progress = int(user_block.completed_lessons) / int(block.number_of_lessons) * 100
            users_progress[block.id] = round(progress)
        except UserBlock.DoesNotExist:
            users_progress[block.id] = 0
        print(users_progress[block.id])
    print(users_progress)
    print (type(users_progress))

    return render(request, 'lessons/lesson_board.html',
                  {
                      'courses': blocks,
                      'progress': users_progress,
                  })

@login_required(login_url='login')
def lessons_board_view(request, block_id):
    """
    Display all lessons for a specific block with user's performance.

    Args:
        request (HttpRequest): Incoming HTTP request.
        block_id (int): ID of the block whose lessons are displayed.

    Returns:
        HttpResponse: Renders 'lesson_board.html' with lessons and user's results.
    """
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
        'progress': users_progress,
    })

@login_required(login_url='login')
def lesson_view(request, block_id, lesson_id):
    """
    Display a specific lesson and its questions.

    Args:
        request (HttpRequest): Incoming HTTP request.
        block_id (int): ID of the block containing the lesson.
        lesson_id (int): ID of the lesson to display.

    Returns:
        HttpResponse: Renders 'lesson_view.html' with lesson, list of question IDs, and question objects.
    """
    lesson = Lesson.objects.get(id = lesson_id)
    questions = lesson.question_set.all()
    questions_list = list(questions.values_list('id', flat = True))
    questions_dict = {question.id:question for question in questions}

    return render(request, 'lessons/lesson_view.html', {
        'lesson': lesson,
        'questions_list': questions_list,
        'questions_dict': questions_dict,
         })

def check_answer_ajax(request):
    """
    AJAX endpoint to check if a user's answer is correct.

    Expects POST parameters:
        - question_id: ID of the question
        - user_answer: Answer provided by the user

    Returns:
        JsonResponse: {"correct": bool, "correct-answer": str} if valid,
                      {"error": str} with 400 status if invalid.
    """
    if request.method == 'POST':
        question_id = request.POST.get('question_id')
        user_answer = request.POST.get('user_answer')

        question = get_object_or_404(Question, id=question_id)

        result = check_answer(question, user_answer)

        return JsonResponse(result)
    return JsonResponse({'error': 'Invalid request'}, status=400)

def check_answer(question, user_answer):
    """
    Check if a user's answer matches the correct answer.

    Args:
        question (Question): Question object.
        user_answer (str): Answer provided by the user.

    Returns:
        dict: {"correct": bool, "correct-answer": str}
    """
    if question.question_type == 'W':
        is_correct = user_answer.lower().strip() == question.correct_answer.lower().strip()
    else:
        is_correct = user_answer == question.correct_answer


    return {"correct": is_correct, "correct-answer": question.correct_answer}
@csrf_exempt
def save_user_performance(request):
    """
    Save user's lesson performance and update streaks.

    Expects a JSON body with:
        - result (int): User's result in the lesson.
        - lesson_id (int): ID of the lesson.
        - block (int): ID of the block.
        - mistakes (list[int]): IDs of questions answered incorrectly.

    Updates:
        - UserLesson: Stores result for the lesson.
        - UsersAnswers: Records incorrectly answered questions.
        - UserBlock: Updates block progress.
        - User streak: Updates streak if user is authenticated.

    Returns:
        JsonResponse: {'status': 'success'} on success,
                      {'status': 'error', 'message': str} on error,
                      or 405 if the method is not POSTed.
    """
    if request.method== 'POST':
        try:
            data = json.loads(request.body)
            result = data.get('result')
            lesson_id = data.get('lesson_id')
            lesson = Lesson.objects.get(id = lesson_id)
            block_id = data.get('block')
            block = Block.objects.get(id = block_id)

            mistaken_questions_id = data.get('mistakes')
            questions = Question.objects.filter(id__in = mistaken_questions_id)

            UserLesson.objects.update_or_create(
                user=request.user,
                lesson= lesson,
                defaults={
                    'result': int(result)
                }
            )
            update_streak(request.user)

            for question in questions:
                UsersAnswers.objects.update_or_create(
                    user = request.user,
                    if_correct = False,
                    lesson = lesson,
                    block = block,
                    question= question,
                )

            UserBlock.objects.update_or_create(
                user=request.user,
                block = block
            )
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error'}, status=405)
