import assistant as ast
from assistant import VirtualAssistant
import pytest

@pytest.fixture(scope='module')
def assistant():
    print('-------setup---------')
    assistant = VirtualAssistant()
    return assistant


# NOTE: These tests can vary as some results are subject to change over time
@pytest.mark.parametrize('search_word, result', [
    ("what is the size of the earth", "3,958.8 mi"),
    ('cosine of 30', '0.15425144988'),
    ('what is the capital city of spain', 'Madrid'),
    ('who is the best soccer in the world', 'lionel messis'),
    ('what is cancer', 'A disease in which abnormal cells divide uncontrollably and destroy body '
                        'tissue.'),
    ('who was nikola tesla', 'Nikola Tesla was a SerbianAmerican inventor, electrical engineer, mechanical '
                                'engineer, and futurist who is best known for his contributions to the design '
                                'of the modern alternating current electricity supply system. ')
])
def test_search_question(assistant, search_word, result):
    assert assistant.search_question(search_word).lower() == result.lower()


def test_greeting():
    assert ast.greeting('hi larry') == "hi" or "hello" or "hola" or \
           "greetings" or "hey there" or "hey" or "howdy"

def test_how_are_you():
    assert ast.how_are_you() == "good. how are you?" or "fine. and you?" or \
    "can't complain. how are you?" or "great. and you?"

@pytest.mark.parametrize('result', [
    ("How does a rabbi make coffee? Hebrews it."),
    ("I have many jokes about unemployed people, sadly none of them work."),
    ("What’s the difference between a G-spot and a golf ball? A man will actually search for a golf ball."),
    ("How did I quit smoking? I decided to smoke only after sex."),
    ("How do you spot a blind man on a nude beach? It’s not hard.")
])
def test_jokes(result):
    assert ast.jokes() == result












