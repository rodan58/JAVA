# модуль для тестирования, и матемматический модуль
import pytest
import math

import formula_gerona


class TestFormulaGerona:

    def test_sqrt(self):
    	# создаём объект для вычисления квдартного корня
        rs = formula_gerona.SquareRoot()
        # берём значения от 0 до 99
        for value in range(0, 100):
        	# результат из стандартной функции sqrt(), берём за 
        	# верный ответ
            res_1 = math.sqrt(value)
            # результат нащей функции
            res_2 = rs.sqrt(value)
            # сравниваем результаты, числа с точностью до 5 знаков
            # после запятой, должны быть равны
            assert round(res_1, 5) == round(res_2, 5)
        # check Exeption
        # проверяем исключение, функция не должна принимать отрицательные
        # значения
        with pytest.raises(ValueError):
            rs.sqrt(-1)

