from number import NUMBER
from natasha.extractors import Extractor

class NumberExtractor(Extractor):
    def __init__(self):
        super(NumberExtractor, self).__init__(NUMBER)

    def replace(self, text):
        new_text = ""
        start = 0
        if text:
            for match in self.parser.findall(text):
                if match.fact.multiplier:
                    num = match.fact.int * match.fact.multiplier
                else:
                    num = match.fact.int
                new_text += text[start: match.span.start] + str(num)
                start = match.span.stop
            new_text += text[start:]
            if start == 0:
                return text
            else:
                return new_text
        else:
            return None
