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
        Замена чисел в тексте без их группировки

        Аргументы:
            text: исходный текст

        Результат:
            new_text: текст с замененными числами
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
        Замена сгруппированных составных чисел в тексте

        Аргументы:
            text: исходный текст

        Результат:
            new_text: текст с замененными числами
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


    def replace_groups_sa(self, text):
        """
        Замена сгруппированных составных чисел в тексте и отдельно стоящих чисел без их суммирования

        Аргументы:
            text: исходный текст

        Результат:
            new_text: текст с замененными числами
        """
        groups = self._get_groups(text)
        new_text = ''
        start = 0
        for group in groups:
            new_text += text[start: group[1]]

            nums = []
            prev_tz = 0
            prev_mult = None
            for match in group[0]:
                mult = match.multiplier if match.multiplier else 1
                curr_num = match.int
                tz = self.trailing_zeros(curr_num)
                if (tz < prev_tz) and (mult >= prev_mult) and curr_num != 0  and (self.n_digits(curr_num) < self.n_digits(nums[0][0])):
                    nums[0] = (nums[0][0] + curr_num, mult)
                else:
                    nums.insert(0, (curr_num, mult))
                prev_mult = mult
                prev_tz = tz

            prev_mult = None
            new_nums = []
            for num, mult in nums:
                if not prev_mult or mult <= prev_mult:
                    new_nums.append(num * mult)
                else:
                    new_nums[-1] += num * mult
                prev_mult = mult

            new_nums.reverse()
            new_text += ' '.join(map(str, new_nums))
            start = group[2]
            
        new_text += text[start:]
        
        return new_text
