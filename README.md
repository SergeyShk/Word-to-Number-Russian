# Word-to-Number (Russian)

Проект для перевода чисел, записанных в текстовом виде на русском языке.

## Необходимые библиотеки

* **yargy**;
* **natasha**.

Установка библиотек:

`$ pip install yargy natasha`

## Структура проекта

* **number.py** - грамматики для текстового представления чисел;
* **extractor.py** - класс для извлечения чисел.

## Пример использования

Код:

```python
text = "Выплаты за второго и третьего ребенка выросли на 5 десятых процента и составили девяносто тысяч рублей"
extractor = NumberExtractor()

for match in extractor(text):
    print(match.fact)

print(extractor.replace(text))
```

Результат:

```shell
Number(int=2, multiplier=None)
Number(int=3, multiplier=None)
Number(int=5, multiplier=0.1)
Number(int=90, multiplier=1000)
Выплаты за 2 и 3 ребенка выросли на 0.5 процента и составили 90000 рублей
```