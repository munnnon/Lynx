from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Block(models.Model):
    name = models.CharField(max_length=255)
    users = models.ManyToManyField(User, through='UserBlock', related_name='blocks')

    def __str__(self):
        return self.name

    @property
    def number_of_lessons (self):
        return self.lesson_set.count

class Lesson(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=500)
    block = models.ForeignKey(Block, on_delete=models.CASCADE)
    users = models.ManyToManyField(User, through='UserLesson', related_name='lessons')


    def __str__(self):
        return self.name

class UserBlock(models.Model):
    block = models.ForeignKey(Block, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'block' )

    @property
    def completed_lessons(self):
        return UserLesson.objects.filter(
            user = self.user,
            lesson__block = self.block,
            result__gte = 75
        ).count()

    @property
    def is_completed(self):
        total_lessons = self.block.number_of_lessons
        return self.completed_lessons>=total_lessons

    def __str__(self):
        return f"{self.user} completed {self.completed_lessons} in {self.block}"

class UserLesson(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    result= models.IntegerField

    class Meta:
        unique_together = ('user', 'lesson')

    def __str__(self):
        return f"{self.user} completed {self.lesson} with {self.result} result"


class Question(models.Model):
    abcd_question = 'ABCD'
    written_question = 'W'
    true_false_question = 'TF'
    questions_types = [
        (abcd_question, 'One choice'),
        (written_question, 'Written answer'),
        (true_false_question, 'TrueFalse')
    ]
    content = models.CharField(max_length=255)
    question_type = models.CharField(max_length=4, choices=questions_types, default=written_question)
    answer_variants = models.CharField(max_length=400)
    correct_answer = models.TextField(max_length=100)
    users = models.ManyToManyField(User, through='UsersAnswers', related_name='questions')
    lessons = models.ManyToManyField(Lesson)

    def __str__(self):
        return self.content


class UsersAnswers(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    if_correct = models.BooleanField
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    block = models.ForeignKey(Block, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'question')

    def __str__(self):
        return f"{self.user} answer {self.question} corect({self.if_correct}) from lesson {self.lesson} in the block {self.block}"