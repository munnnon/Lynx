import django.utils.timezone
from django.contrib.auth.models import User
from django.db import models


class Streak(models.Model):
    """Model that stores information about user's consecutive activity"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='streak')
    start_date = models.DateField(auto_now_add=True)
    last_activity_date = models.DateField(default= None, null=True)
    days_count = models.PositiveIntegerField(default=0)

    @classmethod
    def get_streak(cls, user):
        """
        Retrieve or create a streak for the given user.

        Args:
            user (User): The user instance.

        Returns:
            streak (Streak): the streak instance for the given user.
        """
        streak, _ = cls.objects.get_or_create(user = user)
        return streak

    def __str__(self):
        return str(self.days_count)

