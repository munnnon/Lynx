import random
from datetime import date

from django.shortcuts import render

from .models import Translation


def get_daily_words(request):
     today = date.today().toordinal()
     total_words = Translation.objects.count()

     if total_words<= 3:
          random_words = list(Translation.objects.all())
     else:
          random_ids = random.Random(today).sample(range(total_words), 3)
          random_words = list(Translation.objects.filter(id__in = random_ids))

     daily_words = []
     for word in random_words:
          daily_words.append((word.word, word.translation_polish))

     return render(request, "dictionaries/lynx.html", {'daily_words': daily_words})


def main_view(request):
     return render(request, 'dictionaries/lynx.html', {})