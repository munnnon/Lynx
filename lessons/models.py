from datetime import timezone

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Block(models.Model):
    """Model that represents a block of lessons."""

    name = models.CharField(max_length=255)
    users = models.ManyToManyField(User, through='UserBlock', related_name='blocks')

    @property
    def number_of_lessons(self):
        """
        Count the number of lessons in the given block.

        Returns:
            int: number of lessons in the block
        """

        return self.lesson_set.count()

    def __str__(self):
        return self.name



class Lesson(models.Model):
    """Represents a single lesson that belongs to a block."""

    name = models.CharField(max_length=255)
    description = models.TextField(max_length=500)
    block = models.ForeignKey(Block, on_delete=models.CASCADE)
    users = models.ManyToManyField(User, through='UserLesson', related_name='lessons')


    def __str__(self):
        return self.name

class UserBlock(models.Model):
    """Intermediate model tracking a user's progress within a block."""

    block = models.ForeignKey(Block, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'block' )

    @property
    def completed_lessons(self):
        """
        Counts the number of completed lessons within a block. The success threshold for the lesson is 75%.

        Returns:
            int: number of completed lessons
        """

        return UserLesson.objects.filter(
            user = self.user,
            lesson__block = self.block,
            result__gte = 75
        ).count()

    @property
    def is_completed(self):
        """
        Check if all lessons within a block are completed.

        Returns:
            boolean: if block is completed
        """

        total_lessons = self.block.number_of_lessons
        return self.completed_lessons>=total_lessons

    def __str__(self):
        return f"{self.user} completed {self.completed_lessons} in {self.block}"

class UserLesson(models.Model):
    """Intermediate model storing a user's result in a lesson."""

    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    result= models.IntegerField( default= 0)
    completed_at = models.DateField (auto_now= True)

    class Meta:
        unique_together = ('user', 'lesson')

    def __str__(self):
        return f"{self.user} completed {self.lesson} with {self.result} result"


class Question(models.Model):
    """Represents a question that can belong to one or more lessons."""

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
    """Intermediate model that stores a user's mistaken answer to a question."""

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    if_correct = models.BooleanField(default= False)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    block = models.ForeignKey(Block, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'question')

    def __str__(self):
        return f"{self.user} answer {self.question} corect({self.if_correct}) from lesson {self.lesson} in the block {self.block}"