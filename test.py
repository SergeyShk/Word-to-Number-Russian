import pytest
from extractor import NumberExtractor

@pytest.fixture(scope='module')
def extractor():
    return NumberExtractor()

tests = [
    (
        "Я купил сорок пять килограмм картошки и 7 пудов моркови", 
        "Я купил 45 килограмм картошки и 7 пудов моркови"
    ),
    (
        "Выплаты за второго-третьего ребенка выросли на девять сотых процента", 
        "Выплаты за 2-3 ребенка выросли на 0.09 процента"
    ),
    (
        "Девятьсот восемьдесят семь тысяч шестьсот пятьдесят четыре минус 321", 
        "987654 минус 321"
    ),
    (
        "Госдолг США в тысяча девятьсот пятидесятом году составил двести пятьдесят шесть миллиардов девятьсот миллионов долларов", 
        "Госдолг США в 1950 году составил 256900000000 долларов"
    )
]

@pytest.mark.parametrize('test', tests)
def test_extractor(extractor, test):
    text, etalon = test
    guess = extractor.replace_groups(text)
    assert guess == etalon