from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Block(models.Model):
    name = models.CharField(max_length=255)
    number_of_lessons = models.IntegerField
    users = models.ManyToManyField(User, through='UserBlock', related_name='blocks')

    def __str__(self):
        return self.name

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
    completed_lessons = models.PositiveIntegerField
    if_completed = models.BooleanField

    class Meta:
        unique_together = ('user', 'block' )

    def __str__(self):
        return f"{self.user} completed {self.completed_lessons} in {self.block}"

class UserLesson(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    result = models.IntegerField

    class Meta:
        unique_together = ('user', 'lesson')

    def __str__(self):
        return f"{self.user} completed {self.lesson} with {self.result} result"

