import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Lynx.settings')
django.setup()
from lessons.models import Block, Lesson, Question
from texts.models import Text

def clear_existing_data():
    """Usuwa wszystkie istniejące dane"""
    Question.objects.all().delete()
    Lesson.objects.all().delete()
    Block.objects.all().delete()
    Text.objects.all().delete()
    print("Usunięto wszystkie istniejące pytania, lekcje, bloki, teksty")


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
            "question_type": "W",
            "correct_answer": "u/ó",
            "lessons": [lessons[0]],
            "answer_variants": ""
        },
        {
            "content": "Jak brzmi ta litera:'Е'?",
            "question_type": "W",
            "correct_answer": "je",
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
            "content": "Jak powiedzieć 'Dzień dobry' po białorusku?",
            "question_type": "ABCD",
            "answer_variants": "Добры дзень|Добрай раніцы|Да пабачэння|Добрай ночы",
            "correct_answer": "Добры дзень",
            "lessons": [lessons[1], lessons[2]]
        },
        {
            "content": "Jak brzmi liczba 5 po białorusku?",
            "question_type": "ABCD",
            "answer_variants": "Чатыры|Пяць|Шэсць|Сем",
            "correct_answer": "Пяць",
            "lessons": [lessons[1]]
        },
        {
            "content": "Jak zapytać 'Ile to kosztuje?' po białorusku?",
            "question_type": "W",
            "correct_answer": "Колькі гэта каштуе?",
            "lessons": [lessons[2]],
            "answer_variants": ""
        },
        {
            "content": "W języku białoruskim istnieją rodzajniki określone",
            "question_type": "TF",
            "correct_answer": "False",
            "lessons": [lessons[3]],
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
                      "— Да заў-тра./n — Да сус-трэ-чы."
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
    # clear_existing_data()
    create_blocks()
    create_lessons()
    create_questions()
    create_texts()