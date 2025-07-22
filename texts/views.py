from django.shortcuts import render, get_object_or_404

from .models import Text


def get_list_of_texts(request):
    search_query = request.GET.get('search', '')

    if request.method == 'GET':

        list_of_texts = Text.objects.filter(name__icontains= search_query)
        return render(request, "texts/list_of_texts.html",
                      {'list_of_texts': list_of_texts, 'search_query': search_query})
    else:
        list_of_texts = Text.objects.all()
    return render(request, "texts/list_of_texts.html",  {'list_of_texts':list_of_texts})

def get_text(request, text_id):
    text = get_object_or_404(Text, id = text_id)
    return render(request, 'texts/reading_text.html', {'text':text})
