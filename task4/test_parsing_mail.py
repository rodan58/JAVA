# тесты на pytest для parsing_mail.py
#
#

import pytest	# модуль для тестирования
import os.path	# модуль для работы с путями

# импортируем что будем тестировать
from parsing_mail import Mail, MailParser


# переменная с названием тестового файла,
# маленький файл с письмами, полной путь до папки
TEST_FILE = os.path.join(os.path.dirname(__file__), "mails.txt")


class TestMail:

	def test_search_paramter(self):
		# считываем строки из файла
		with open(TEST_FILE) as file:
			 lines = file.readlines()
		# на основе строк, создаём text для письма
		mail_text = "".join(lines[0:62]).strip()
		# создаём объект письма
		mail = Mail(mail_text)
		# правильные значения которые должны содержаться в text письма
		# первое значение имя параметра, второе его значение 
		# ручками достали эти данные из тестого файла
		values = (
			("Author", "stephen.marquard@uct.ac.za"),
			("X-DSPAM-Probability", "0.0000"),
			("X-DSPAM-Confidence", "0.8475"),
			)
		# сверяем параметры и их значения
		for parameter, answer in values:
			# параметр должен быть в списке параметров для объекта Mail
			assert parameter in mail.parameters
			# значение параметра должно равняться ответу
			assert mail.params_n_values[parameter] == answer


class TestMailParser:

	def test_search_mails(self):
		with open(TEST_FILE) as file:
			 lines = file.readlines()
		# созаём text для объектов Mail, ручками посчитав границы текстов
		mail_text_1 = "".join(lines[0:62]).strip()
		mail_text_2 = "".join(lines[65:127]).strip()
		mail_text_3 = "".join(lines[130:191]).strip()
		mp = MailParser(TEST_FILE)	# создаём парсер
		# сверяем текста писем (объекты Mail) и текста которые должны быть
		for mail, text in zip(mp.mails, 
							[mail_text_1, mail_text_2, mail_text_3]):
			# текста, должны быть идентичны
			# texts have to equal
			assert mail.text == text
		# количество писем должно совпадать с количеством text-ов для них
		# length of texts have to aqual
		assert len(mp.mails) == 3

	def test_append_correct_mail(self):
		# сичтываем строки файла
		with open(TEST_FILE) as file:
			 lines = file.readlines()
		# на основе строк, создаём корректный текст для объекта Mail
		# т.е. со всеми нужными параметрами "Author", "X-DSPAM-Probability"
		correct_text = "".join(lines[0:62]).strip()
		not_correct_text = ""	# и не правильный, без нужных параметров
		mp = MailParser(TEST_FILE) # создаём объект парсера
		# lenght of mails have to change
		# запоминаем количество объектов Mail, добавляем один объект письма
		# он должен доавиться, если количество писем увеличилось на 1 то ok
		old_len = len(mp.mails)	
		mp.append_correct_mail(correct_text)
		assert len(mp.mails) == old_len + 1
		# length of mails have to not change
		# всё тоже самое, только с неправильным text для Mail, 
		# объект Mail, не должен добаиться, а значит количество объектов
		# не ложно поменяться
		old_len = len(mp.mails)	
		mp.append_correct_mail(not_correct_text)
		assert len(mp.mails) == old_len

	def test_search_average_X_DSPAM_Probability(self):
		mp = MailParser(TEST_FILE)
		# change values of paramters
		# в парсере (mp) список (mails) из трёх объектов Mail всем объектам
		# меняем параметр "X-DSPAM-Probability" на другие  значения
		for mail, value in zip(mp.mails, ("2", "2", "2")):
			mail.params_n_values["X-DSPAM-Probability"] = value
		# create value for new parameters
		# мы изменили значения параметров писем
		# значит вычисляем новое значение среднее "X-DSPAM-Probability" 
		mp.search_average_X_DSPAM_Probability()
		assert mp.average_X_DSPAM_Probability == 2.0
		# check function if parser has no mails
		# проверяем что бы не возникло ошибки если мы будем вычислять
		# значение на основе пустого списка писем
		mp.mails = []
		mp.search_average_X_DSPAM_Probability()
		assert mp.average_X_DSPAM_Probability == None
	
	def test_count_authors_n_mails(self):
		mp = MailParser(TEST_FILE) # создаём парсер
		# берём text из одного из писем, что бы text был корректным
		mail_text_example = mp.mails[0].text
		# вспомогательный словарь на основе которого мы будем создавать
		# список mails с объектами Mail
		# ключ - значение параметра "Author", значение - количество писем
		authors = {
			'stephen.marquard@uct.ac.za': 3,
			'louis@media.berkeley.edu': 2,
			'zqian@umich.edu': 1,
			}
		# опустошаем список писем, дабы не мешался
		mp.mails = []
		# create mails with variety avtors
		# создаём новый список mails
		# для каждого автора и количества писем от него
		for author, number in authors.items():
			# создаём письма с этим автором нужное кол-во раз
			for i in range(1, number + 1):
				# на основе корректного text создаём объект Mail
				mail = Mail(mail_text_example)
				# в этом объекте меняем автора и добавляем к другим письмам
				mail.params_n_values["Author"] = author
				mp.mails.append(mail)
		# создаём вспомогательный словарь authors_n_mails
		mp.count_authors_n_mails()
		# словари должны быть одинаковы
		assert mp.authors_n_mails == authors
		# if parser has no mails
		# проверка на случай если писем нет в mails
		mp.mails = []
		mp.count_authors_n_mails()
		assert mp.authors_n_mails == {}

	def test_count_spamers(self):
		mp = MailParser(TEST_FILE) # создаём парсер
		# берём текст одного из писем, пригодиться для создания аналогичных
		mail_text_example = mp.mails[0].text
		# значения, название спамера
		# строка со значением для "X-DSPAM-Confidence" и 
		# логическое True/False (спамер/нет)
		values = (
			("A", "0.9000", True),
			("B", "0.0000", False),
			("C", "0.8000", False),
			("D", "0.9900", True),
			)
		# опустошаем список писем
		mp.mails = []
		# создаём список mails объектов Mail с нужными значениями 
		# "X-DSPAM-Confidence" для каждого письма
		for author, value in [tpl[:2] for tpl in values]:
			# создаём объект Mail на основе корректного text
			mail = Mail(mail_text_example)
			# создаём новое значение для "Author"
			mail.params_n_values["Author"] = author
			# добавляем нужную строку из values
			mail.params_n_values["X-DSPAM-Confidence"] = value
			mp.mails.append(mail)
		mp.count_spamers()	# считаем спамеров (создаём список spamers)
		# сверяем каждое письмо с правильным результатом
		for mail, is_spamer in zip(mp.mails, [tpl[2] for tpl in values]):
			# если автор в спамерах и ответ совпадает с нужным, то ok
			assert (mail.params_n_values["Author"] in mp.spamers) == is_spamer
		# spamers without duplicate
		# проверяем список спамеров, на наличие повторений
		# создаём несколько одинаковых писем, с одинаковыми авторами
		# и созначениями подходящими под спам
		mp.mails = []	# удаляем предыдущие письма
		for i in range(2):	# create some the same spamers 
			mail = Mail(mail_text_example) # создаём письмо
			# у этого письма меняем автора, и значения для вычисления спама
			mail.params_n_values["Author"] = 'stephen.marquard@uct.ac.za'
			mail.params_n_values["X-DSPAM-Confidence"] = '0.9000'
			mp.mails.append(mail)	# добавляем к списку писем
		mp.count_spamers()	# высичтываем кол-во спамеров
		# их не должно быть большего одного, т.к. автор писем один
		assert len(mp.spamers) == 1
