# Программа о лифтах
# - выполнить в стиле ООП
# - три лифта, 9 этажей
# - на первом этаже всегда должен быть свободный лифт


class Elevator:
    """класс представляет объект лифта"""
    
    def __init__(self):
        """Имеет поле floor (int) - в котором номер этажа"""
        self.floor = 1

class ElevatorSystem:

    def __init__(self, number_of_floors, number_of_elevators):
        """ Объект системы управления лифтами
        number_of_floors (int) - число этажей в здании
        number_of_elevators (int) - число лифтов

        Поля объекта:
        elevators (list) - список лифтов (объекты Elevator)
        """
        self.number_of_floors = number_of_floors
        self.number_of_elevators = number_of_elevators
        self.elevators = []
        # создаём нужное количество лифтов
        for i in range(self.number_of_elevators):
            # создаём и добавляем один лифт
            # по умолчанию при создании лифтов, все находятся на
            # первом этаже
            self.elevators.append(Elevator())

    def call_elevator(self, floor):
        """Вызывает лифт на указанный этаж floor (int)"""
        # находим самый ближайший лифт
        elevator = self.search_nearest_elevator(floor)
        # меняем "вызываем" на нужный этаж
        elevator.floor = floor
        # если на первом этаже нет лифта, то
        if not self.is_there_elevator_on_first_floor():
            # находим самый ближайший для первого этажа лифт
            # без того который уже вызывали, и найденный лифт "вызываем"
            # на первый этаж
            elevator_for_fist_floor = self.search_nearest_elevator(
                1, without=[elevator])
            elevator_for_fist_floor.floor = 1

    def search_nearest_elevator(self, floor, without=[]):
        """Возвращает объект лифта (Elevator) самый близкий к этажу
            floor. without (list) - список лифтов (Elevator) которые 
            проверять не нужно.
        """
        # список лифтов, без тех которые указанны в without
        elevators = filter(lambda elevator: elevator not in without,
                           self.elevators)
        # находим ближайший лифт, к указанному этажу
        # сортируем список по (этаж лифта - нужный этаж), значение делаем
        # положительным. Из отсортированного списка берум первый лифт
        nearest_elevator = sorted(
            elevators,
            key=lambda elevator: abs(floor - elevator.floor))[0]
        return nearest_elevator

    def is_there_elevator_on_first_floor(self):
        """Возращает True, если на первом этаже есть лифт, иначе False"""
        # если в списке лифтов есть хотя бы один с номером этажа 1
        if any(map(lambda elevator : elevator.floor == 1,
                   self.elevators)):
            return True
        return False


if __name__ == "__main__":
    # система лифтов
    elsys = ElevatorSystem(9, 3)
    # можно вызвать лифт при помощи:
    # elsys.call_elevator(int)   
