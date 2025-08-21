import random
from datetime import date

from django.shortcuts import render

from accounts.views import update_streak
from .models import Translation


def get_daily_words(request):
     """
     Retrieves a set of daily words for the main page.

     - Selects 3 random words from the Translation model.
     - If there are fewer than or equal to 3 words, returns all words.
     - If the user is authenticated, updates their learning streak.

     Args:
        request (HttpRequest): The incoming HTTP request.

     Returns:
        HttpResponse: Renders the "lynx.html" template with a context containing
                      'daily_words', which is a list of tuples (word, translation_polish).
     """
     today = date.today().toordinal()
     total_words = Translation.objects.count()

     if total_words<= 3:
          random_words = list(Translation.objects.all())
     else:
          ids = list(Translation.objects.values_list('id', flat=True))
          random_ids = random.Random(today).sample(ids, 3)
          random_words = list(Translation.objects.filter(id__in = random_ids))

     daily_words = []
     for word in random_words:
          daily_words.append((word.word, word.translation_polish))

     if request.user.is_authenticated:
          update_streak(request.user)

     return render(request, "dictionaries/lynx.html", {'daily_words': daily_words})
