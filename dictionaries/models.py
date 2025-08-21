from django.db import models


class Translation(models.Model):
    """Model that stores words and their translation in English and Polish."""
    word = models.CharField(max_length=255)
    translation_english = models.CharField(max_length=255, null=True)
    translation_polish = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.word

