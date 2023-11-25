import nltk
from nltk.corpus import stopwords
import pymorphy2
import re
from collections import Counter
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context



# скачивание глобальных штук
nltk.download('stopwords')
MORPH = pymorphy2.MorphAnalyzer()


ADDITIONAL_STOPWORDS = [
    'a', 'about', 'all', 'am', 'an', 'and', 'any', 'are', 'as', 'at', 'be',
    'been', 'but', 'by', 'can', 'could', 'do', 'for', 'from', 'has', 'have',
    'i', 'if', 'in', 'is', 'it', 'me', 'my', 'no', 'not', 'of', 'on', 'one',
    'or', 'so', 'that', 'the', 'them', 'there', 'they', 'this', 'to', 'was',
    'we', 'what', 'which', 'will', 'with', 'would', 'you', 'а', 'будем', 'будет',
    'будете', 'будешь', 'буду', 'будут', 'будучи', 'будь', 'будьте', 'бы', 'был',
    'была', 'были', 'было', 'быть', 'в', 'вам', 'вами', 'вас', 'весь', 'во', 'вот',
    'все', 'всё', 'всего', 'всей', 'всем', 'всём', 'всеми', 'всему', 'всех', 'всею',
    'всея', 'всю', 'вся', 'вы', 'да', 'для', 'до', 'его', 'едим', 'едят', 'ее',
    'её', 'ей', 'ел', 'ела', 'ем', 'ему', 'емъ', 'если', 'ест', 'есть', 'ешь',
    'еще', 'ещё', 'ею', 'же', 'за', 'и', 'из', 'или', 'им', 'ими', 'имъ', 'их',
    'к', 'как', 'кем', 'ко', 'когда', 'кого', 'ком', 'кому', 'комья', 'которая',
    'которого', 'которое', 'которой', 'котором', 'которому', 'которою', 'которую',
    'которые', 'который', 'которым', 'которыми', 'которых', 'кто', 'меня', 'мне',
    'мной', 'мною', 'мог', 'моги', 'могите', 'могла', 'могли', 'могло', 'могу',
    'могут', 'мое', 'моё', 'моего', 'моей', 'моем', 'моём', 'моему', 'моею',
    'можем', 'может', 'можете', 'можешь', 'мои', 'мой', 'моим', 'моими', 'моих',
    'мочь', 'мою', 'моя', 'мы', 'на', 'нам', 'нами', 'нас', 'наса', 'наш', 'наша',
    'наше', 'нашего', 'нашей', 'нашем', 'нашему', 'нашею', 'наши', 'нашим', 'нашими',
    'наших', 'нашу', 'не', 'него', 'нее', 'неё', 'ней', 'нем', 'нём', 'нему', 'нет',
    'нею', 'ним', 'ними', 'них', 'но', 'о', 'об', 'один', 'одна', 'одни', 'одним',
    'одними', 'одних', 'одно', 'одного', 'одной', 'одном', 'одному', 'одною', 'одну',
    'он', 'она', 'оне', 'они', 'оно', 'от', 'по', 'при', 'с', 'сам', 'сама', 'сами',
    'самим', 'самими', 'самих', 'само', 'самого', 'самом', 'самому', 'саму', 'свое',
    'своё', 'своего', 'своей', 'своем', 'своём', 'своему', 'своею', 'свои', 'свой',
    'своим', 'своими', 'своих', 'свою', 'своя', 'себе', 'себя', 'собой', 'собою',
    'та', 'так', 'такая', 'такие', 'таким', 'такими', 'таких', 'такого', 'такое',
    'такой', 'таком', 'такому', 'такою', 'такую', 'те', 'тебе', 'тебя', 'тем',
    'теми', 'тех', 'то', 'тобой', 'тобою', 'того', 'той', 'только', 'том', 'томах',
    'тому', 'тот', 'тою', 'ту', 'ты', 'у', 'уже', 'чего', 'чем', 'чём', 'чему',
    'что', 'чтобы', 'эта', 'эти', 'этим', 'этими', 'этих', 'это', 'этого', 'этой',
    'этом', 'этому', 'этот', 'этою', 'эту', 'я', 'мені', 'наші', 'нашої', 'нашій',
    'нашою', 'нашім', 'ті', 'тієї', 'тією', 'тії', 'теє', 'очень', 'вновь', 'казаться',
    'nan', 'всё', 'это', 'твой', 'свой', 'весь', 'вообще',
    'пусть', 'ещё', 'который', 'её', 'словно', 'пока',
    'сколько', 'сквозь', 'чей', 'вокруг', 'любой', 'слишком', 'почему',
    'среди', 'значит', 'ваш', 'тысяча', 'однажды', 'сегодня',
    'завтра', 'вчера', 'послезавтра', 'позавчера', 'нибыть', 'точно',
    'уметь', 'целый', 'полный', 'часть', 'делать',
    'готовый', 'хотя', 'как', 'столько', 'равно', 'оно', 'похожий',
    'скоро', 'разный', 'всякий', 'порой', 'часто', 'настоящий', 'вместо',
    'вовсе', 'иметь', 'вроде', 'лишь', 'также', 'млн', 'руб',
    'наверное', 'три', 'четыре', 'пять', 'шесть', 'семь', 'восемь',
    'девять', 'десять', 'пускай', 'мимо', 'частый', 'сей', 'привет',
    'наверно', 'туда', 'иль', 'возможно', 'вено', 'иной', 'едва',
    'поэтому', 'впереди', 'зря', 'вообще', 'меж', 'мол', 'нету', 'наш',
    'иначе', 'всякий', 'ради', 'оттого', 'нечего', 'скорее',
    'пред', 'сначала', 'вряд', 'случайно', 'коль', 'многий', 'кроме',
    'откуда', 'нынче', 'ибо', 'порою', 'вне', 'кой', 'еле', 'разом',
    'либо', 'зато', 'сорок', 'везде', 'таков', 'вон', 'покуда',
    'затем', 'особенно', 'несмотря', 'сотый', 'всюду',
    'возле', 'кстати', 'прям', 'ныне', 'бай', 'предельно',
    'чрез', 'некий', 'впредь', 'практически', 'лишь', 'каждый',
    'день', 'год', 'мочь', 'коли', 'найти', 'нужно', 'снова',
]

EDUCATIONAL_STOPWORDS = [
    "друг", "коллега", "блок", "лекция", "семинар", "вебинар", "урок", "курс",
    "модуль", "тренинг", "практикум", "мастер-класс", "туториал", "студент",
    "преподаватель", "лектор", "учитель", "обучающийся",
    "группа", "класс", "аудитория", "куратор", "задание", "проект",
    "домашний", "работа", "экзамен", "тест", "оценка", "дедлайн", "кредит",
    "аттестация", "сертификация", "учебный", "план", "образовательная",
    "программа", "академическая степень", "научное", "исследование", "материал",
    "методические указания", "учебник", "литература", "конспект", "основы",
    "понимание", "случай", "идея", "задание", "тема", "первый", "второй",
    "практика", "чиселка", "лайфхак", "понятие", "плюсик", "профессия"
]

GARBAGE = [
    "внимание", "штука", "текст", "текст", "страничка", "color", "центр",
    "доллар", "стиль", "отступ", "файл", "экран", "пример", "hello", "значение",
    "этап"
]

ALL_STOPWORDS = stopwords.words('russian') + \
                stopwords.words('english') + \
                ADDITIONAL_STOPWORDS + \
                EDUCATIONAL_STOPWORDS + \
                GARBAGE


# правило — последовательность слов (список) с их частями речи и падежами
MORPH_RULES = [
    [{"POS": "NOUN", "case": ["nomn", "accs"]}],
    [{"POS": "ADJF", "case": ["nomn", "accs"]}, {"POS": "NOUN", "case": ["nomn", "accs"]}],
    [{"POS": "NOUN", "case": ["nomn", "accs"]}, {"POS": "NOUN", "case": ["gent"]}],
    [{"POS": "NOUN", "case": ["nomn", "accs"]}, {"POS": "ADJF", "case": ["gent"]}, {"POS": "NOUN", "case": ["gent"]}],
    [{"POS": "ADJF", "case": ["nomn", "accs"]}, {"POS": "ADJF", "case": ["nomn", "accs"]}, {"POS": "NOUN", "case": ["nomn", "accs"]}],
    [{"POS": "ADJF", "case": ["nomn", "accs"]}, {"POS": "NOUN", "case": ["nomn", "accs"]}, {"POS": "NOUN", "case": ["gent"]}]
]

ENGLISH_RULE = re.compile("[A-Za-z\d-]{3,}(?:\s+[A-Za-z\d-]{3,})*")


def match_morph_rule(text, rule):
    global MORPH

    result = False
    words = text.split()
    if len(words) != len(rule):
        return False
    flag = False
    for word, rule_part in zip(words, rule):
        parsed = MORPH.parse(word)[0]
        if parsed.tag.POS != rule_part["POS"]:
            flag = True
        if parsed.tag.case not in rule_part["case"]:
            flag = True
    if not flag:
        result = True
    return result


def exclude_stopwords(tokens):
    global ALL_STOPWORDS

    return [word for word in tokens if word.lower() not in ALL_STOPWORDS]


def preprocess(text, lowercase=True):
    text = text.replace("\n", "")
    text = re.sub(r"( - |- )", r" ", text)
    text = re.sub(r"\b(\w+)( \1\b)+", r"\1", text)
    text = re.sub(r"([0-9]+).([0-9]+)", "", text)
    text = re.sub(r"([0-9]+).(\s+)", "", text)
    text = re.sub(r"[:\.,»«)(\n\t–]", ". ", text)
    text = re.sub(r"([а-яa-zё]+)([А-ЯA-ZЁ]+)", r"\1. \2", text)
    text = re.sub(r"([0-9]+)(\s+)([0-9]+)", "", text)
    text = re.sub(r"\.(\s+)([a-zA-Zа-яА-ЯёЁ0-9\-])", lambda x: x.group(0).upper(), text)
    text = text.replace("\xa0", " ")
    text = text.replace(".", ". ").strip()
    if lowercase:
        return re.findall(r'\b\w+\b', text.lower())
    return re.findall(r'\b\w+\b', text)


def find_english_terms(text):
    global ENGLISH_RULE

    return list(ENGLISH_RULE.findall(text))


def find_morph_terms(text, remove_stopwords=True):
    global MORPH_RULES

    terms = []
    tokens = preprocess(text)
    if remove_stopwords:
        tokens = exclude_stopwords(tokens)

    for i in range(len(tokens)):
        eng_result = find_english_terms(' '.join(tokens[i:i+3]))
        if eng_result:
            terms.extend(eng_result)
        for rule in MORPH_RULES:
            phrase = ' '.join(tokens[i:i+len(rule)])
            if match_morph_rule(phrase, rule):
                terms.append(phrase)
    return terms


# strong: если хотя бы один из токенов термина — стопслово, то удаляем термин
# иначе удаляем только токен, оставляем остаток термина
def filter_terms(terms, strong=False):
    global MORPH
    global ALL_STOPWORDS

    filtered_terms = []

    for term in terms:
        words = term.split()
        normalized_words = [MORPH.parse(word)[0].normal_form for word in words]
        if strong:
            if not any(word in ALL_STOPWORDS for word in normalized_words):
                filtered_terms.append(term)
        else:
            result = ' '.join([words[i] for i in range(len(words)) if normalized_words[i] not in ALL_STOPWORDS])
            if result != "":
                filtered_terms.append(result)

    return filtered_terms


def get_terms_candidates(text, strong=False):
    terms = find_morph_terms(text)

    return filter_terms(list(terms), strong=strong)


def normalize_terms(words):
    global MORPH

    return [MORPH.parse(word)[0].normal_form for word in words]


def normalize_frequencies(frequencies):
    max_freq = max(frequencies.values())
    return {term: freq / max_freq for term, freq in frequencies.items()}


def filter_terms_by_frequency(terms, threshold=0.15):
    term_frequencies = Counter(terms)
    normalized_frequencies = normalize_frequencies(term_frequencies)
    filtered_terms = {term: freq for term, freq in normalized_frequencies.items() if freq >= threshold}
    return filtered_terms


def finalize_terms(terms, filtered_terms):
    return [term for term in terms if term in filtered_terms.keys()]
