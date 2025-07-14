from django.db import models

from django.contrib.auth import get_user_model
from lessons.models import Lesson, Block

User = get_user_model()

class Question(models.Model):
    abcd_question = 'ABCD'
    written_question = 'W'
    true_false_question = 'TF'
    questions_types = [
        (abcd_question, 'One choice'),
        ( written_question, 'Written answer'),
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
        unique_together = ('user', 'question' )

    def __str__(self):
        return f"{self.user} answer {self.question} corect({self.if_correct}) from lesson {self.lesson} in the block {self.block}"