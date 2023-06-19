#
import pytest

from SMA_and_median_filter import SMA, MF


class TestSMA:

	def test_create_results(self):
		# значения для объекта простой скользящей средней
		values = (
			{
				"window_size": 2, 
				"numbers": [2, 4, 1, 2], 
				"results": [3.0, 2.5, 1.5]
				},
			{
				"window_size": 3, 
				"numbers": [3, 4, 2, 0, 1], 
				"results": [3.0, 2.0, 1.0]
				},
			)
		for sma_dict in values:
			sma = SMA(sma_dict["window_size"])
			assert sma_dict["results"] == \
					sma.create_results(sma_dict["numbers"])
	
	def test_create_windows(self):
		values = (
			{
				"window_size": 2,
				"numbers": [2, 4, 1, 2], 
				"windows": [(2, 4), (4, 1), (1, 2)],
				},
			{
				"window_size": 3,
				"numbers": [2, 4, 1, 2], 
				"windows": [(2, 4, 1), (4, 1, 2)],
				},
			)
		for sma_dict in values:
			sma = SMA(sma_dict["window_size"])
			assert sma_dict["windows"] == \
					sma.create_windows(sma_dict["numbers"])


	def test_create_one_value(self):
		# проверяем как алгоритм находит среднее значение окна
		# при разном размере окна
		sma_2 = SMA(2)
		assert 0.5 == sma_2.create_one_value([0, 1])
		sma_3 = SMA(3)
		assert 2.0 == sma_3.create_one_value([0, 1, 5])
		sma_4 = SMA(3)
		assert 2.0 == sma_4.create_one_value([0, 1, 5, 2])


class TestMF:

	def test_create_results(self):
		# Пример вычисления медианного фильтра:
		# x = [2 80 6 3]
		# 
		#     y[1] = медиана[2 2 80] = 2
		#     y[2] = медиана[2 80 6] = медиана[2 6 80] = 6
		#     y[3] = медиана[80 6 3] = медиана[3 6 80] = 6
		#     y[4] = медиана[6 3 3] = медиана[3 3 6] = 3
		# 
		# и в итоге:
		# 
		# y = [2 6 6 3] — выход медианного фильтра 		#
		# значения для проверки
		values = (
			{
			# массив = [2, 4, 1, 7]
			# окно - 2
			# (7*) - дополненное значение
			# [2, 4] = (2 + 4) / 2 = 3.0
			# [4, 1] = (4 + 1) / 2 = 2.5
			# [1, 7] = (1 + 7) / 2 = 4.0
			# [7, 7*] = (7 + 7) / 2 = 7.0
			# 
			# результат: 
			# 	[2, 3, 2.5, 4]
				"window_size": 2, 
				"numbers": [2, 4, 1, 7], 
				"results": [3.0, 2.5, 4.0, 7.0],
			},
			{
			# массив = [2, 4, 1, 7]
			# окно - 3
			# (2*) - дополненное значение
			# [2*, 2, 4] = [2, 2, 4] = 2
			# [2, 4, 1] = [1, 2, 4] = 2
			# [4, 1, 7] = [1, 4, 7] = 4
			# [1, 7, 7*] = 7
			# 
			# результат: 
			# 	[2, 2, 4, 7]
				"window_size": 3, 
				"numbers": [2, 4, 1, 7], 
				"results": [2, 2, 4, 7],
			},
			{
			# массив = [2, 4, 1, 7]
			# окно - 4
			# (2*) - дополненное значение
			# [2*, 2, 4, 1] = [1, 2, 2, 4] = (2 + 2) / 2 = 2.0
			# [2, 4, 1, 7] = [1, 2, 4, 7] = (2 + 4) / 2 = 3.0
			# [4, 1, 7, 7*] = [1, 4, 7, 7] = (4 + 7) / 2 = 5.5
			# [1, 7, 7*, 7*] = (7 + 7) / 2 = 7.0
			# результат: 
			# 	[2, 3, 5.5, 7]
				"window_size": 4, 
				"numbers": [2, 4, 1, 7], 
				"results": [2.0, 3.0, 5.5, 7.0],
			},
			)
		for mf_dict in values:
			mf = MF(mf_dict["window_size"])
			assert mf_dict["results"] == \
					mf.create_results(mf_dict["numbers"])

	def test_create_windows(self):
		values = (
			{
				"window_size": 2,
				"numbers": [2, 4, 1], 
				"windows": [(2, 4), (4, 1), (1, None)],
				},
			{
				"window_size": 3,
				"numbers": [2, 4, 1], 
				"windows": [(None, 2, 4), (2, 4, 1), (4, 1, None)],
				},
			)
		for mf_dict in values:
			mf = MF(mf_dict["window_size"])
			assert mf_dict["windows"] == \
					mf.create_windows(mf_dict["numbers"])


	def test_create_one_value(self):
		# создаём объекты MF, с разными значениями окна (window_size)
		# и у каждого объкта вызываем функцию для нахождения одного
		# медианного значения
		mf_2 = MF(2)
		assert mf_2.create_one_value([1, 2]) == 1.5
		mf_3 = MF(3)
		assert mf_3.create_one_value([3, 1, 5]) == 3
		mf_4 = MF(4)
		assert mf_4.create_one_value([4, 2, 3, 6]) == 3.5

	def test_replacing_empty_values(self):
		# Проверям замену пустых значений в списке чисел
		mf_5 = MF(5)
		values = (
			([], []),
			([1, 2], [1, 2]),
			([None, 2], [2, 2]),
			([2, None], [2, 2]),
			([None, None, 3], [3, 3, 3]),
			([3, None, None], [3, 3, 3]),
			([None, 1, 2], [1, 1, 2]),
			([1, 2, None], [1, 2, 2]),
			)
		for window, right_answer in values:
			assert mf_5.replacing_empty_values(window) == right_answer
