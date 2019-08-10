from yargy import rule, or_
from yargy.pipelines import morph_pipeline, caseless_pipeline
from yargy.interpretation import fact, const
from yargy.predicates import eq, caseless, normalized, type

Number = fact('Number', ['int', 'multiplier'])
NUMS_RAW = {
    'ноль': 0,
    'нуль': 0,
    'один': 1, 
    'два': 2, 
    'три': 3, 
    'четыре': 4, 
    'пять': 5,
    'шесть': 6,
    'семь': 7,
    'восемь': 8,
    'девять': 9,
    'десять': 10,
    'одиннадцать': 11,
    'двенадцать': 12,
    'тринадцать': 13,
    'четырнадцать': 14,
    'пятнадцать': 15,
    'шестнадцать': 16,
    'семнадцать': 17,
    'восемнадцать': 18,
    'девятнадцать': 19,
    'двадцать': 20,
    'тридцать': 30,
    'сорок': 40,
    'пятьдесят': 50,
    'шестьдесят': 60,
    'семьдесят': 70,
    'восемьдесят': 80,
    'девяносто': 90,
    'сто': 100,
    'двести': 200,
    'триста': 300,
    'четыреста': 400,
    'пятьсот': 500,
    'шестьсот': 600,
    'семьсот': 700,
    'восемьсот': 800,
    'девятьсот': 900,
    'тысяча': 10**3,
    'миллион': 10**6,
    'миллиард': 10**9,
    'триллион': 10**12,
}
DOT = eq('.')
INT = type('INT')
THOUSANDTH = rule(caseless_pipeline(['тысячных', 'тысячная'])).interpretation(const(10**-3))
HUNDREDTH = rule(caseless_pipeline(['сотых', 'сотая'])).interpretation(const(10**-2))
TENTH = rule(caseless_pipeline(['десятых', 'десятая'])).interpretation(const(10**-1))
THOUSAND = or_(
    rule(caseless('т'), DOT),
    rule(caseless('тыс'), DOT.optional()),
    rule(normalized('тысяча')),
    rule(normalized('тыща'))
).interpretation(const(10**3))
MILLION = or_(
    rule(caseless('млн'), DOT.optional()),
    rule(normalized('миллион'))
).interpretation(const(10**6))
MILLIARD = or_(
    rule(caseless('млрд'), DOT.optional()),
    rule(normalized('миллиард'))
).interpretation(const(10**9))
TRILLION = or_(
    rule(caseless('трлн'), DOT.optional()),
    rule(normalized('триллион'))
).interpretation(const(10**12))
MULTIPLIER = or_(
    THOUSANDTH,
    HUNDREDTH,
    TENTH,
    THOUSAND,
    MILLION,
    MILLIARD,
    TRILLION
).interpretation(Number.multiplier)
NUM_RAW = rule(morph_pipeline(NUMS_RAW).interpretation(Number.int.normalized().custom(NUMS_RAW.get)))
NUM_INT = rule(INT).interpretation(Number.int.custom(int))
NUM = or_(
    NUM_RAW,
    NUM_INT
).interpretation(Number.int)
NUMBER = or_(
    rule(NUM, MULTIPLIER.optional())
).interpretation(Number)