from django.urls import path
from .import views

urlpatterns = [
    path("", views.get_list_of_texts, name='list_of_texts'),
    path("/<int:text_id>", views.get_text, name='get_text')
]