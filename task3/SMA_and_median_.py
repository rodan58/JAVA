# Задание 3 – Скользящие средние
# 
# Разработайте и докажите корректность работы алгоритма 
# простой скользящей средней (Simple Moving Average, SMA), 
# медианного фильтра. 
# Требования:
# 1.	Данные на вход поступают по одному значению.
# 2.	Размер окна задается пользователем. 
# 3.	Графики значений до и после обработки постройте любым 
# 			доступным способом.
# 4.	Количество исходных значений не менее 25.
# 5.	Способы ввода: загрузка из интернета, загрузка из файла.
#
import itertools
import matplotlib.pyplot as plt

class SMA:
	"""Объект алгоритма для вычисления простой скользящей средней SMA.
	"""
	def __init__(self, window_size, numbers=[]):
		"""Объект для вычисления простой скользящей средней для списка
			чисел (numbers)
				window_size - размер "окна"
				numbers - список чисел
				window - "окно", список чисел длинной в window_size
				results - результат работы алгоритма
		"""
		self.window_size = window_size
		self.numbers = numbers
		self.window = []
		self.results = []
	
	def create_results(self):
		"""Создаёт новый список (results), на основе (numbers)"""
		self.results = []
		for number in self.numbers:
			self.add_one_number(number, False)
	
	def add_one_number(self, number, add_to_numbers=True):
		"""Добавляем одно число (number) и вычисляем среднее значение
			"окна" (window) размер которого (window_size), добавляет
			результат в (results)
			number - число которое мы хотим добавить
			add_to_numbers - для добавления числа в основной список
				(numbers), внутри create_results вызывать только с False
				иначе бесконечный вызов
		"""
		# добавляем к основным числам (numbers), если это нужно
		if add_to_numbers:
			self.numbers.append(number)
		# добавляем число в "окно"
		self.window.append(number)
		# если количество чисел в "онке" меньше размера "окна", то пропуск
		if len(self.window) < self.window_size:
			return
		# если размер "окна" стал больше допустимого, убераем первое число
		if len(self.window) > self.window_size:
			self.window.pop(0)
		# вычислем среднее значение для "окна" (списока чисел)
		window_average = round(sum(self.window) / self.window_size, 2)
		self.results.append(window_average)
		# print(f"window = {self.window}\nwindow_size = {self.window_size}")
		# print(f"numbers = {self.numbers}\nresults = {self.results}")


class MF:
	"""Алгоритм Медианный Фильтр"""

	def __init__(self, window_size, numbers=[]):
		"""Объект алгоритма медианной фильтрации
			window_size - размер окна
			numbers - список чисел, для нахождения медианных значений
			results - список медианных значений, создаётся при вызове
						create_results()
			half - половина от размера окна, для внутренний вычислений
			even - чётность размера окна (window_size)
		"""
		self.window_size = window_size
		self.numbers = numbers
		self.half = window_size // 2
		self.even = bool(window_size % 2 == 0)
		self.results = []

	def create_results(self):
		"""Создаёт новый список медианных значений (results) , 
		на соновании значений из списка (numbers)"""
		self.results = []
		# дополняем список слева и с права значениями None
		numbers = [None] * (self.half - self.even) + self.numbers \
					+ [None] * (self.half)
		# print(f"numbers: {numbers}")
		# создаём на основе списка numbers, итераторы
		# их должно быть столько же сколько размер окна (window_size)
		iterators = itertools.tee(numbers, self.window_size)
		# все кроме первого итератора сдвигаем.
		# т.е. каждый последующий итератор будет начинаться со следующего
		# элемента например:
		# 	window_size = 3
		# 	numbers = [None, 1, 2, 3, None]
		# 	iterators = (iterator1, iterator2, iterator3)
		# 	iterator1 = [None, 1, 2, 3, None]
		# 	iterator2 = [1, 2, 3, None]
		# 	iterator3 = [2, 3, None]
		# 
		for i, iterator in enumerate(iterators):
			for j in range(1, i + 1):
				iterator.__next__()
		# Создаём окна при помоши генераторов, например
		# 	window_size = 3
		# 	numbers = [None, 1, 2, 3, None]
		# 	windows = (window1, window2, window3)
		# 	window1 = [None, 1, 2]
		# 	window2 = [1, 2, 3]
		# 	window3 = [2, 3, None]
		# 
		for window in zip(*iterators):
			# из кортежа, создаём список, иначе ошибка в create_one_median()
			window = list(window)
			# вычисляем медианное значение на основе окна
			median = self.create_one_median(list(window))
			# добавляем в конечный результат
			self.results.append(median)
		# print(vars())
		# print(self.__dict__)
		pass

	def create_one_median(self, window):
		"""Принмает список чисел (window), длина списка должна равняться
			размеру окна (len(window) == self.window_size)

		"""
		# обрабатываем окно, все значения None, заменяются на 
		# ближайшее значение
		window = self.replacing_empty_values(window)
		# сортиурем числа по возрастанию
		sorted_window = sorted(window)
		# находим медианное значение, т.е. среднее число отсортированного
		# списка
		center_value = sorted_window[self.half - self.even]
		# если размер окна (window_size) чётный (even), то найди среднее
		# значение между медианными значениями
		if self.even:
			center_value = (center_value + sorted_window[self.half]) / 2
		# print(f"window: {window}\ncenter_value: {center_value}")
		return center_value

	def replacing_empty_values(self, window):
		"""Заменяет значения None в списке (window), на крайнее значение
			например 	[None, 1, 2] -> [1, 1, 2]
						[1, 2, None] -> [1, 2, None]
		"""
		# если нет пустых значений (None), то верни список чисел
		if all(window):
			return window
		# вычисляем список чисел без None, первое число, последнее,
		real_values = list(filter(lambda v: v != None, window))
		first_value, last_value = real_values[0], real_values[-1]
		# флаг если число было, нужен для заполнения крайних значений
		# если False, то значения None заполняем, первым числом (левым) в
		# списке, инае, последним (правым)
		real_number_was = False
		# перебираем индексы (i) и элементы списка (value)
		for i, value in enumerate(window):
			if value == None:			# если значение None
				if real_number_was:		# если было число, а не None
					window[i] = last_value	# Заполняем значения None 
				else:						# крайним левым числом
					window[i] = first_value # иначе крайним правым
				continue	# перезодим к следующему значению
			# если это число, а не None, то меняем флаг
			real_number_was = True
		# print(vars())
		return window


class MovingAverages:

	def __init__(self, filename):
		"""Создаём объект для создания графиков алгоритмов
			filename - название файла с данными
		"""
		# извлекаем значения из файла, сохраняем в numbers
		with open(filename) as file:
			self.numbers = list(map(lambda x: int(x), file.read().split()))

	def __call__(self, window_sizes=[3, 5]):
		"""Создаём графики
			window_sizes - размеры окнон для графиков
		"""
		data_sma = self.create_objects(window_sizes, SMA)
		data_mf = self.create_objects(window_sizes, MF)
		self.show_plot([self.numbers] + data_sma,
			"SMA\nwindows: " + ",".join(map(str, window_sizes)))
		self.show_plot([self.numbers] + data_mf, 
			"Median Filter\nwindows: " + ",".join(map(str, window_sizes)))

	def create_objects(self, window_sizes, Class):
		"""Создаём объекты класса Class, с размерами окон (window_sizes)
			Возвращает список списков для графиков
		"""
		data = []
		for window_size in window_sizes:
			obj = Class(window_size, self.numbers)
			obj.create_results()
			data.append(obj.results)
		return data

	def show_plot(self, data=[], plot_name=""):
		"""Создаёт график на основе списков в data, 
		с указанным названием (plot_name)
		"""
		for values in data:
			plt.plot(values)
		plt.title(plot_name)
		plt.show()


if __name__ == "__main__":
	ma = MovingAverages("data2.txt")
	# рисуем графики для SMA, MF, с разными размерами окон
	ma([3, 5, 10])
