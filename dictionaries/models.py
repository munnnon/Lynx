from django.db import models


class Translation(models.Model):
    word = models.CharField(max_length=255)
    translation = models.CharField(max_length=255)

    def __str__(self):
        return self.word

