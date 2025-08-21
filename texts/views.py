from django.shortcuts import render, get_object_or_404

from .models import Text


def get_list_of_texts(request):
    """
    Display a list of texts, optionally filtered by a search query.

    If a 'search' GET parameter is provided, filters texts whose names
    contain the query string (case-insensitive). Otherwise, returns all texts.

    Args:
        request (HttpRequest): Incoming HTTP request, may include a 'search' GET parameter.

    Returns:
        HttpResponse: Renders 'list_of_texts.html' with a list of texts and the search query if provided.
    """
    search_query = request.GET.get('search', '')

    if search_query == '':
        list_of_texts = Text.objects.all()
    else:
        list_of_texts = Text.objects.filter(name__icontains= search_query)
        return render(request, "texts/list_of_texts.html",{
            'list_of_texts': list_of_texts,
            'search_query': search_query
        })
    return render(request, "texts/list_of_texts.html", {'list_of_texts': list_of_texts})


def get_text(request, text_id):
    """
    Display a single text by its ID.

    Args:
        request (HttpRequest): Incoming HTTP request.
        text_id (int): The ID of the text to display.

    Returns:
        HttpResponse: Renders 'reading_text.html' with the selected text.
    """
    text = get_object_or_404(Text, id=text_id)
    return render(request, 'texts/reading_text.html', {'text':text})
