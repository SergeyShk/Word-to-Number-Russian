# Word-to-Number (Russian)

Проект для перевода чисел, записанных в текстовом виде на русском языке.

## Необходимые библиотеки

* **yargy**;
* **natasha**.

Установка библиотек:

`$ pip install -r requirements.txt`

## Структура проекта

* **number.py** - грамматики для текстового представления чисел;
* **extractor.py** - класс для извлечения чисел;
* **test.py** - модуль тестирования.

## Пример использования

Код:

```python
text = "Выплаты за второго-третьего ребенка выросли на пятьсот двадцать пять тысячных процента и составили 90 тысяч рублей"
extractor = NumberExtractor()

for match in extractor(text):
    print(match.fact)

print(extractor.replace(text))
print(extractor.replace_groups(text))
```

Результат:

```shell
Number(int=2, multiplier=None)
Number(int=3, multiplier=None)
Number(int=500, multiplier=None)
Number(int=20, multiplier=None)
Number(int=5, multiplier=0.001)
Number(int=90, multiplier=1000)
Выплаты за 2-3 ребенка выросли на 500 20 0.005 процента и составили 90000 рублей
Выплаты за 2-3 ребенка выросли на 0.525 процента и составили 90000 рублей
```
