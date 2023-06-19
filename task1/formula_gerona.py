#
#


class SquareRoot:

    def __init__(self):
        pass

    def sqrt(self, number):
        """Метод для вычисления квадратного корня из числа number
            с использованием формулы Герона
        """
        # если чило отрицательное, возбуждаем исключение
        if number < 0:
            raise ValueError("number cannot be less than 0")
        # если число равно 0, то верни резульата 0.0
        if number == 0:
            return 0.0
        # запоминаем число
        self.number = number
        # запускаем итарецию (подбор чисел которые могут быть ответом)
        res = self._iter(1.0)
        # округляем результат, если это нужно
        if (res - int(res)) < 0.001:
           return round(res, 1)
        return res

    def _iter(self, answer):
        """answer - предпологаемый ответ"""
        # если предпологаемый ответ является верным, то возвращаем его
        if self._is_right_answer(answer):
            return answer
        # 
        else:
            return self._iter(self._improve(answer))
        
    def _improve(self, answer):
        """"Улучшаем" ответ, т.е. изменяем значение предпологаемого
            ответа, теперь answer будет хранить среднее между
            answer и number
        """
        return self._average(answer, self.number / answer)
    
    def _average(self, x, y):
        """Возвращает среднее между двумя значениями"""
        return (x + y) / 2
    
    def _is_right_answer(self, answer):
        """Если answer - достаточно точным является ответом, 
            для нахождения квадратного корня (number), то верни True, 
            иначе False
        """
        if(abs(answer**2 - self.number) < 0.000001):
            return True
        else:
            return False
        

sr = SquareRoot()
