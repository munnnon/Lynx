import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Lynx.settings')
django.setup()
from lessons.models import Block, Lesson, Question
from texts.models import Text
from dictionaries.models import Translation

def clear_existing_data():
    """Usuwa wszystkie istniejące dane"""
    Question.objects.all().delete()
    Lesson.objects.all().delete()
    Block.objects.all().delete()
    Text.objects.all().delete()
    Translation.objects.all().delete()
    print("Usunięto wszystkie istniejące pytania, lekcje, bloki, teksty i słowa")

def load_initial_dictionary():
    dictionary_data = [
        {"word": "Мама", "translation_polish": "Mama", "translation_english": "Mom / Mother"},
        {"word": "Тата", "translation_polish": "Tata", "translation_english": "Dad / Father"},
        {"word": "Брат", "translation_polish": "Brat", "translation_english": "Brother"},
        {"word": "Сястра", "translation_polish": "Siostra", "translation_english": "Sister"},
        {"word": "Цёця", "translation_polish": "Ciocia", "translation_english": "Aunt"},
        {"word": "Дзядзька", "translation_polish": "Wujek", "translation_english": "Uncle"},
        {"word": "Дзядуля", "translation_polish": "Dziadek", "translation_english": "Grandfather"},
        {"word": "Бабуля", "translation_polish": "Babcia", "translation_english": "Grandmother"},
        {"word": "Стрыечны брат/сястра", "translation_polish": "Kuzyn/kuzynka", "translation_english": "Cousin (male/female)"},
        {"word": "Вітаю", "translation_polish": "Witam", "translation_english": "Hello"},
        {"word": "Вітанкі", "translation_polish": "Cześć", "translation_english": "Hi"},
        {"word": "Дзякуй", "translation_polish": "Dziękuję", "translation_english": "Thank you"},
        {"word": "Дзякаваць", "translation_polish": "Dziękować", "translation_english": "To thank"},
        {"word": "Я", "translation_polish": "Ja", "translation_english": "I"},
        {"word": "Ты", "translation_polish": "Ty", "translation_english": "You (singular)"},
        {"word": "Ён", "translation_polish": "On", "translation_english": "He"},
        {"word": "Яна", "translation_polish": "Ona", "translation_english": "She"},
        {"word": "Яно", "translation_polish": "Ono", "translation_english": "It"},
        {"word": "Мы", "translation_polish": "My", "translation_english": "We"},
        {"word": "Вы", "translation_polish": "Wy", "translation_english": "You (plural/formal)"},
        {"word": "Спадар/Спадарыня", "translation_polish": "Pan/Pani", "translation_english": "Mr./Mrs."},
        {"word": "Добры дзень", "translation_polish": "Dzień dobry", "translation_english": "Good day / Hello"},
        {"word": "Добры вечар", "translation_polish": "Dobry wieczór", "translation_english": "Good evening"},
        {"word": "Пакуль", "translation_polish": "Cześć", "translation_english": "Bye"},
        {"word": "Да пабачэння", "translation_polish": "Do zobaczenia", "translation_english": "See you"},
        {"word": "Дабранач", "translation_polish": "Dobranoc", "translation_english": "Good night"},
        {"word": "Добрай ночы", "translation_polish": "Dobrej nocy", "translation_english": "Good night (formal)"},
        {"word": "Да заўтра", "translation_polish": "Do jutra", "translation_english": "See you tomorrow"},
        {"word": "Усяго добрага", "translation_polish": "Wszystkiego dobrego", "translation_english": "All the best"},
        {"word": "Так", "translation_polish": "Tak", "translation_english": "Yes"},
        {"word": "Не", "translation_polish": "Nie", "translation_english": "No"},
        {"word": "Калі ласка", "translation_polish": "Proszę", "translation_english": "Please"},
        {"word": "Прабач/Прабачце", "translation_polish": "Przepraszam", "translation_english": "Sorry / Excuse me"},
        {"word": "На спажытак", "translation_polish": "Proszę bardzo", "translation_english": "You're welcome"},
        {"word": "На здароўе", "translation_polish": "Na zdrowie", "translation_english": "Bless you / You're welcome"},
        {"word": "Сам", "translation_polish": "Sam", "translation_english": "Alone / Himself"},
        {"word": "Сама", "translation_polish": "Sama", "translation_english": "Alone /Herself"},
        {"word": "Само", "translation_polish": "Samo", "translation_english": "Alone /Itself"},
        {"word": "Самі", "translation_polish": "Sami/Same", "translation_english": "Alone / Themselves"},
        {"word": "Вядомы", "translation_polish": "Znany", "translation_english": "Known / Famous"},
        {"word": "Прыгожы", "translation_polish": "Piękny", "translation_english": "Beautiful"},
        {"word": "Шчаслівы", "translation_polish": "Szczęśliwy", "translation_english": "Happy"},
        {"word": "Стомлены", "translation_polish": "Zmęczony", "translation_english": "Tired"},
        {"word": "Дрэнны", "translation_polish": "Zły", "translation_english": "Bad"},
        {"word": "Добры", "translation_polish": "Dobry", "translation_english": "Good"}
    ]
    for word in dictionary_data:
        Translation.objects.get_or_create(**word)
    print("Zaktualizowano słownik")

def create_blocks():
    blocks_data = [
        {"name": "Alfabet"},
        {"name": "Podstawy"},
        {"name": "Codzienne zwroty"},
        {"name": "Gramatyka"},
    ]

    for block_data in blocks_data:
        Block.objects.get_or_create(**block_data)
    print("Zaktualizowano bloki")


def create_lessons():
    blocks = Block.objects.all()

    lessons_data = [
        {"name": "Samogłoski", "description": "Nauka samogłosek w języku białoruskim", "block": blocks[0]},
        {"name": "Spółgłoski", "description": "Nauka spółgłosek w języku białoruskim", "block": blocks[0]},
        {"name": "Powitania", "description": "Nauka podstawowych powitań w języku białoruskim", "block": blocks[1]},
        {"name": "Liczby 1-10", "description": "Nauka liczb od 1 do 10", "block": blocks[1]},
        {"name": "W sklepie", "description": "Zwroty przydatne podczas zakupów", "block": blocks[2]},
        {"name": "Rodzajniki", "description": "Nauka rodzajników w języku białoruskim", "block": blocks[3]},
    ]

    for lesson_data in lessons_data:
        Lesson.objects.get_or_create(
            name = lesson_data['name'],
            defaults=lesson_data
        )
    print("Zaktualizowano lekcje")


def create_questions():
    lessons = Lesson.objects.all()

    questions = [
        {
            "content": "Jak brzmi ta litera:'A'?",
            "question_type": "W",
            "correct_answer": "a",
            "lessons":[lessons[0]],
            "answer_variants": ""
        },
        {
            "content": "Jak brzmi ta litera:'O'?",
            "question_type": "W",
            "correct_answer": "o",
            "lessons": [lessons[0]],
            "answer_variants": ""
        },
        {
            "content": "Jak brzmi ta litera:'Я'?",
            "question_type": "W",
            "correct_answer": "ja",
            "lessons": [lessons[0]],
            "answer_variants": ""
        },
        {
            "content": "Jak brzmi ta litera:'У'?",
            "question_type": "ABCD",
            "correct_answer": "u/ó",
            "lessons": [lessons[0]],
            "answer_variants": "u/ó|y|ju|o"
        },
        {
            "content": "Czy litera:'Е' brzmi jak 'e' w języku polskim?",
            "question_type": "TF",
            "correct_answer": "False",
            "lessons": [lessons[0]],
            "answer_variants": ""
        },
        {
            "content": "Jak brzmi ta litera:'Э'?",
            "question_type": "W",
            "correct_answer": "e",
            "lessons": [lessons[0]],
            "answer_variants": ""
        },
        {
            "content": "Jak brzmi ta litera:'Ю'?",
            "question_type": "W",
            "correct_answer": "ju",
            "lessons": [lessons[0]],
            "answer_variants": ""
        },
        {
            "content": "Jak brzmi ta litera:'Ё'?",
            "question_type": "W",
            "correct_answer": "jo",
            "lessons": [lessons[0]],
            "answer_variants": ""
        },
        {
            "content": "Jak brzmi ta litera:'Б'?",
            "question_type": "W",
            "correct_answer": "b",
            "lessons": [lessons[1]],
            "answer_variants": ""
        },
        {
            "content": "Jak brzmi ta litera:'В'?",
            "question_type": "ABCD",
            "correct_answer": "w",
            "lessons": [lessons[1]],
            "answer_variants": "b|d|w|f"
        },
        {
            "content": "Jak brzmi ta litera:'Г'?",
            "question_type": "W",
            "correct_answer": "gh",
            "lessons": [lessons[1]],
            "answer_variants": ""
        },
        {
            "content": "Jak powiedzieć 'Dzień dobry' po białorusku?",
            "question_type": "ABCD",
            "answer_variants": "Добры дзень|Добрай раніцы|Да пабачэння|Добрай ночы",
            "correct_answer": "Добры дзень",
            "lessons": [lessons[2]]
        },
        {
            "content": "Jak brzmi liczba 5 po białorusku?",
            "question_type": "ABCD",
            "answer_variants": "Чатыры|Пяць|Шэсць|Сем",
            "correct_answer": "Пяць",
            "lessons": [lessons[3]]
        },
        {
            "content": "Jak zapytać 'Ile to kosztuje?' po białorusku?",
            "question_type": "W",
            "correct_answer": "Колькі гэта каштуе?",
            "lessons": [lessons[4]],
            "answer_variants": ""
        },
        {
            "content": "W języku białoruskim istnieją rodzajniki określone",
            "question_type": "TF",
            "correct_answer": "False",
            "lessons": [lessons[5]],
            "answer_variants": ""
        },
    ]

    for question_data in questions:
        related_lessons = question_data.pop('lessons', [])
        question, created = Question.objects.get_or_create(
            content=question_data['content'],
            defaults= question_data
        )
        if created:
            question.lessons.add(*related_lessons)

    print(f"ZAktualizowano pytania: dodano {len(questions)} nowych pytań")


def create_texts():
    texts_data = [
        {
            "name":"Пас-ля за-нят-каў",
            "content":"Скон-чы-лі-ся за-нят-кі.\n"
                      " Дзе-ці а-пра-ну-лі-ся і па-ча-лі раз-віт-вац-ца.\n"
                      " Пе-ця ска-заў:\n"
                      "— Да па-ба-чэн-ня, Ка-ця-ры-на І-ва-наў-на.\n"
                      " Ко-ля пра-мо-віў:\n "
                      "— Уся-го до-бра-га.\n"
                      " Ма-ша па-жа-да-ла ўсім:\n"
                      " — Бы-вай-це зда-ро-вы.\n "
                      "Ін-шы-я дзе-ці га-ва-ры-лі:\n"
                      " — Уся-го най-леп-ша-га.\n "
                      "— Да заў-тра.\n"
                      " — Да сус-трэ-чы."
        },
        {
            "name": "Podstawowe zwroty",
            "content": "Добры дзень - Dzień dobry\nДобрай раніцы - Dobry ranek\nДа пабачэння - Do widzenia\nДзякуй - Dziękuję"
        },
        {
            "name": "Liczby 1-10",
            "content": "1 - адзін\n2 - два\n3 - тры\n4 - чатыры\n5 - пяць\n6 - шэсць\n7 - сем\n8 - восем\n9 - дзевяць\n10 - дзесяць"
        }
    ]

    for text_data in texts_data:
        Text.objects.get_or_create(
            name='name',
            defaults=text_data
        )
    print("Zaktualizowano teksty")




if __name__ == '__main__':
    clear_existing_data()
    load_initial_dictionary()
    create_blocks()
    create_lessons()
    create_questions()
    create_texts()