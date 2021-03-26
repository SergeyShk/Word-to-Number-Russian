from number import NUMBER
from natasha.extractors import Extractor
import math 


class NumberExtractor(Extractor):
    def __init__(self):
        super(NumberExtractor, self).__init__(NUMBER)


    def n_digits(self, n):
        if n > 0:
            digits = int(math.log10(n)) + 1
        elif n == 0:
            digits = 1
        else:
            digits = int(math.log10(-n)) + 2 # +1 if you don't count the '-'
        
        return digits


    def trailing_zeros(self, n: int):
        """
        Count trailing zeros of a number
        
        Args:
            n: number
        
        Result:
            cnt: count of zeros
        """
        cnt = 0
        while n % 10 == 0 and n != 0:
            cnt += 1
            n = n / 10
        return cnt

    def replace(self, text):
        """
        Replace numerical in text without grouping 

        Args:
            text: initial text

        Result:
            new_text: text with numbers
        """
        if text:
            new_text = ""
            start = 0

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

    def _get_groups(self, text):
        start = 0
        matches = list(self.parser.findall(text))
        groups = []
        group_matches = []

        for i, match in enumerate(matches):
            if i == 0:
                start = match.span.start
            if i == len(matches) - 1:
                next_match = match
            else:
                next_match = matches[i + 1]
            group_matches.append(match.fact)
            if text[match.span.stop: next_match.span.start].strip() or next_match == match:
                groups.append((group_matches, start, match.span.stop))
                group_matches = []
                start = next_match.span.start
        return groups


    def replace_groups(self, text):
        """
        Replace groups of numerical by summation

        Args:
            text: initial text

        Result:
            new_text: text with numbers
        """
        
        groups = self._get_groups(text)
        
        new_text = ""
        start = 0
        for group in groups:
            num = 0
            nums = []
            new_text += text[start: group[1]]
            for match in group[0]:
                curr_num = match.int * match.multiplier if match.multiplier else match.int
                if match.multiplier:
                    num = (num + match.int) * match.multiplier
                    nums.append(num)
                    num = 0
                elif num > curr_num or num == 0:
                    num += curr_num
                else:
                    nums.append(num)
                    num = 0
            if num > 0:
                nums.append(num)
            new_text += str(sum(nums))
            start = group[2]
        new_text += text[start:]

        return new_text
