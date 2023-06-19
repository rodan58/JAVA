# тестируем консольное приложение search_poiynomials.py
# при помощи pytest

import pytest

import search_polynomials


class TestSearchPolynomials:

	def test_create_parser(self):
		"""Проверяем насколько верно парсер разбирает аргументы"""
		# создаём прложение передавая список аргументов
		# (иммитируем запуск из консоли)
		app = search_polynomials.CliApp(['--poly=1,2,3,4,5', '-v', '3'])
		# создаём парсер, т.е. нужные аргументы и прочее
		app.create_parser()
		# в пространстве имён для значений должны быть:
		# строка коэфицентов, такая же какую мы передали
		assert app.namespace.poly[0] == '1,2,3,4,5'
		# также должна быть значение (int) - для знаменателя
		assert app.namespace.v == 3

	def test_extract_values(self):
		"""Проверяем что значения аргументов превратились в нужные
			объекты, т.е. список чисел (poly_values) и целое число (v)
		"""
		# передаём аргументы командной строки
		app = search_polynomials.CliApp(['--poly=1,2', '-v', '3'])
		# создаём парсер
		app.create_parser()
		# извлекаем значения из значений аргументов
		app.extract_values()
		# должны получиться список и одно число
		assert app.poly_values == [1, 2]
		assert app.v == 3

	def test_make_result(self):
		"""Проверяем правильность вычисления результата"""
		# действия аналогичны предыдущим тестам
		app = search_polynomials.CliApp(['--poly=1,2', '-v', '3'])
		app.create_parser()
		app.extract_values()
		# создаём результат из полученных значений
		app.make_result()
		# результат должны совпадать с правильным ответом
		assert app.result == (1/1*3 + 1/2*3)
