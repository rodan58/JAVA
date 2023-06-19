# Задание 4 – Разбор почты

# Программа получает на вход файл: http://www.pythonlearn.com/code3/mbox.txt
# Это журнал принятой почты от разных корреспондентов. 
# Необходимо проанализировать этот файл и узнать:
# 1. Каково среднее значение параметра X-DSPAM-Probability?
# 		Данный параметр представляет число от 0 до 1 и показывает 
#		степень похожести на спам (1 - точно спам).
# 2. Что показывает параметр X-DSPAM-Confidence и как его использовать
#		 для улучшения определения кто спамер?
# 3. Постройте гистограмму по отправителям (отправитель - количество писем)
# 4. Кого стоит заблокировать за спам?) Приведите список, сгенерированный 
# 		кодом по предложенным критериям.

import re   # модуль для работы с регулярными выражениями
import matplotlib.pyplot as plt


class Mail:
    """Класс представляет информацию об одном письме,
        кто отправитель, вероятность того что это спам и пр."""

    def __init__(self, text):
        """ text - текст с информацией о письме
            paramters - список параметров которые должны присутсвовать
            params_n_values - словарь в котором ключ - название 
                параметра, а значение - строка напротив этого параметра
        """
        self.text = text
        self.parameters = [
            "Author", 
            "X-DSPAM-Probability", 
            "X-DSPAM-Confidence",
            ]
        self.params_n_values = dict()
        for parameter in self.parameters:
            self.search_paramter(parameter)

    def search_paramter(self, parameter):
        """Находим значение параметра "parameter" в тексте письма
            при помощи регулярного выражения, если такого параметра нет
            то возбуждается ислючение ValueError, это значит что text
            не содержит нужных параметров.
        """
        p = re.compile(parameter + r": (.+)") # создаём регулярное выражение
        m = p.search(self.text) # находим в тексте совпадение
        if m == None: # если совпадение не найденно, возбуждаем исключение
            raise ValueError("paramter text is not valid")
        # если строка найдена, записываем параметр и его значение
        self.params_n_values[parameter] = m.groups()[0]


class MailParser:
    """Объект для обработки текстового файла с информацией о письмах"""

    def __init__(self, mail_file):
        """"mail_file - имя файла в котором хранятся данные
            
            Все возможные поля:

            mails - список экзэмпляров класса Mail
            spamers - список строк спамеров
            average_X_DSPAM_Probability - среднее значение параметра
        """
        self.mail_file = mail_file
        self.search_mails()
        # self.search_average_X_DSPAM_Probability()

    def search_mails(self):
        """Создаёт новый список спамеров (spamers)"""
        self.mails = []
        # открываем файл и считываем построчно
        with open(self.mail_file) as file:
            new_strings_counter = 0     # счётчик новых (строк символ "\n")
            lines_of_text = []  # список считанный строк из файла
            for line in file.readlines():
                lines_of_text.append(line)
                if line == "\n":    # если пустая строка прибавь счётчик
                    new_strings_counter += 1
                else:               # иначе обнули
                    new_strings_counter = 0 
                # если попалось три строки подряд, то
                if new_strings_counter == 3:
                    new_strings_counter = 0
                    # на основе считанных строк создаём текст для класса Mail
                    text = "".join(lines_of_text).rstrip()
                    # создаём экзэмпляр Mail если text - корректный
                    # и добавляем в, если text содержит нужные параметры
                    self.append_correct_mail(text)
                    lines_of_text = []  # опустошаем список со строками
            # if it is lost mail
            # на случай если строки будут последними в файле,
            # создать на их основе text, и добавить Mail в mails
            else:
                text = "".join(lines_of_text).rstrip()
                self.append_correct_mail(text)

    def append_correct_mail(self, text):
        """Создаёт Mail на сонове text добавляет его в mails,
            если возможно создать экзэпляр Mail на основе text"""
        try:
            mail = Mail(text)
        except ValueError:  # если при создании Mail возникнет исключение
            pass            # то ничего не делай
        else: # если Mail создать удалось, то добавь в mails
            self.mails.append(mail)

    def search_average_X_DSPAM_Probability(self):
        """Создаёт внутри экзэмпляра переменную average_X_DSPAM_Probability
            которая содержит среднее значение параметра X-DSPAM-Probability
            во всех письмах
        """
        # на случай если нет писем
        if not self.mails:
            self.average_X_DSPAM_Probability = None
            return 
        # список в котором все значения типа float из всех писем
        values = [float(mail.params_n_values["X-DSPAM-Probability"]) \
                    for mail in self.mails]
        # print(values)
        # вычисляем саму переменную
        self.average_X_DSPAM_Probability = sum(values) / len(values)

    def count_authors_n_mails(self):
        """Создаёт словарь authors_n_mails в котором ключ - информация
            об авторе письма, а значение - количество писем отправленных
            этим автором. Вспомогательный метод для создания гистограмы
            для отображения количество писем от разных авторов
        """
        self.authors_n_mails = {}
        for mail in self.mails:
            author = mail.params_n_values["Author"] # узнаём автора письма
            try:    # пробуем узнать есть ли этот автор
                self.authors_n_mails[author]
            except KeyError:    # если автор не найден, то создаём
                self.authors_n_mails[author] = 1
            else:               # иначе прибавляем 1
                self.authors_n_mails[author] += 1

    def count_spamers(self):
        """Считаем количество спамеров, записываем авторов в spamers"""
        if not self.mails:  # на случай  если писем нет
            self.spamers = []
            return 
        spamers = set() # множество, для того что бы спамеры не повторялись
        for mail in self.mails:
            # если это спамер, то автора добавляем к спамерам
            if float(mail.params_n_values["X-DSPAM-Confidence"]) >= 0.9:
                spamers.add(mail.params_n_values["Author"])
        self.spamers = list(spamers) # на сонове  множества создаём список

    def show_histogram_with_users(self):
        """Показываем гистограмму авторов и количество отправленных 
            писем, на основе словаря authors_n_mails.
        """
        # сортируем по количеству писем отправленных автором
        # список авторов (names), список количества писем (numbers)
        names = sorted(self.authors_n_mails.keys(), key=lambda v: v)
        numbers = sorted(self.authors_n_mails.values(), key=lambda v: v)
        # создаём гистограмму, выводим
        plt.figure(figsize=(15, 10))
        plt.barh(names, numbers)
        plt.show()


# если запущена эта программа, то выполни код ниже
if __name__ == '__main__':
    # создаём объект парсера писем, передаём название файла с письмами
    # часть работы выполняется при создании парсера:
    # считывание строк файла, создание объектов писем
    mp = MailParser("data3.txt")
    # mp = MailParser("mails.txt")
    mail_1 = mp.mails[0]
    # выполняем все пункты задания
    # 1 task
    mp.search_average_X_DSPAM_Probability()
    print(f"average X-DSPAM-Probability: {mp.average_X_DSPAM_Probability}")
    # 2 task
    print("\"X-DSPAM-Confidence\" shows our confidence that message" +
        "is spam The greater this parameter - the more probable that" + 
        " the message is spam")
    # 3 task
    mp.count_authors_n_mails()
    mp.show_histogram_with_users()
    # 4 task
    mp.count_spamers()
    print("They are spamers: ", mp.spamers)