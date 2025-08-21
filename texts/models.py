from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()


class Text(models.Model):
    """Model for storing texts that can be associated with users."""
    name = models.CharField(max_length=255)
    content = models.TextField(max_length=2000)
    users = models.ManyToManyField(User, through='UserText', related_name='texts')

    def __str__(self):
        return self.name

class UserText(models.Model):
    """Model that tracks when a user has read the given text."""
    text = models.ForeignKey(Text, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    read_at =  models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.text} <- {self.user}"
