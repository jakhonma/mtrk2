TRANSLIT_RULES_LATIN_TO_CYRILLIC = {
    "o'": "ў", "o‘": "ў", "ng": "нг", "Ng": "Нг", "NG": "НГ", "’": "ъ", "yo": "ё", "Yo": "Ё", 
    "YO": "Ё", "yu": "ю",  "Yu": "Ю", "YU": "Ю", "ya": "я", "Ya": "Я", "YA": "Я", "O‘": "Ў", 
    "O'": "Ў", "O‘": "Ў", "g‘": "ғ", "G‘": "Ғ", "G‘": "Ғ", "ch": "ч", "Ch": "Ч", "CH": "Ч", 
    "sh": "ш", "Sh": "Ш", "SH": "Ш", "a": "а", "A": "А", "b": "б", "B": "Б", "d": "д", "D": "Д", 
    "e": "е", "E": "Е", "f": "ф", "F": "Ф", "g": "г", "G": "Г", "h": "ҳ", "H": "Ҳ", "i": "и", 
    "I": "И", "j": "ж", "J": "Ж", "k": "к", "K": "К", "l": "л", "L": "Л", "m": "м", "M": "М", 
    "n": "н", "N": "Н", "o": "о", "O": "О", "p": "п", "P": "П", "q": "қ", "Q": "Қ", "r": "р", 
    "R": "Р", "s": "с", "S": "С", "t": "т", "T": "Т", "u": "у", "U": "У", "v": "в", "V": "В", 
    "x": "х", "X": "Х", "y": "й", "Y": "Й", "z": "з", "Z": "З"
}


TRANSLIT_RULES_CYRILLIC_TO_LATIN = {
    "цио": "tsio", "ае": "aye", 
    "ч": "ch", "Ч": "Ch", "ш": "sh", "щ": "sh", "Ш": "Sh", "Щ": "Sh",
    "нг": "ng", "Нг": "Ng", "ъ": "’", "ь": "", "ё": "yo", "Ё": "Yo", 
    "ю": "yu", "Ю": "Yu", "я": "ya", "Я": "Ya", 
    "ў": "o‘", "Ў": "O‘", "Ў": "O‘", "ғ": "g‘", "Ғ": "G‘",
    "а": "a", "А": "A", "б": "b", "Б": "B", "д": "d", "Д": "D", 
    "е": "e", "Е": "E", "ф": "f", "Ф": "F", "г": "g", "Г": "G", 
    "ҳ": "h", "Ҳ": "H", "и": "i", "И": "I", "ж": "j", "Ж": "J", 
    "к": "k", "К": "K", "л": "l", "Л": "L", "м": "m", "М": "M", 
    "н": "n", "Н": "N", "о": "o", "О": "O", "п": "p", "П": "P", 
    "қ": "q", "Қ": "Q", "р": "r", "Р": "R", "с": "s", "С": "S", 
    "т": "t", "Т": "T", "у": "u", "У": "U", "в": "v", "В": "V", 
    "х": "x", "Х": "X", "й": "y", "Й": "Y", "з": "z", "З": "Z",
    "ц": "s", "Э":'E', "э": 'e'
}


def to_lotin(text: str) -> str:
    """ transliterate(text->str)"""
    for latin, cyrillic in TRANSLIT_RULES_CYRILLIC_TO_LATIN.items():
        text = text.replace(latin, cyrillic)
    return text


def to_cyrillic(text: str) -> str:
    """ transliterate(text->str)"""
    for latin, cyrillic in TRANSLIT_RULES_LATIN_TO_CYRILLIC.items():
        text = text.replace(latin, cyrillic)
    return text
